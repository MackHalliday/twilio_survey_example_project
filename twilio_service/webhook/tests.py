from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
from twilio.twiml.messaging_response import MessagingResponse

from accounts.models import UserProfile
from surveys.models import Question, Survey, UserSurveySubscription, UserResponse
from twilio_service.constant import (
    SURVEY__COMPLETE_RESPONSE,
    SURVEY__CONFIRM_DO_NOT_SEND_RESPONSE,
    SURVEY__CONFIRM_START_RESPONSE,
    SURVEY__NO_SURVEY_AVAILABLE_RESPONSE,
    SURVEY__OPT_OUT_RESPONSE,
    SURVEY__USER_CONFIRM_SURVEY,
    TWILIO__OPT_OUT,
)


class TwilioWebhookTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.user_profile = UserProfile.objects.create(
            user=self.user, phone_number="+123456789"
        )
        self.user_phone_number = self.user_profile.phone_number

        self.survey = Survey.objects.create(survey_name="Test Survey", version=1)
        self.question_1 = Question.objects.create(
            text="Question 1?", survey=self.survey, order=1
        )
        self.question_2 = Question.objects.create(
            text="Question 2?", survey=self.survey, order=2
        )
        self.question_3 = Question.objects.create(
            text="Question 3?", survey=self.survey, order=3
        )

        self.survey_user = UserSurveySubscription.objects.create(
            survey=self.survey, user=self.user, completed=False
        )

        self.client = Client()
        self.webhook_survey_url = reverse("webhook-survey")
        self.content_type = "application/xml"

    def test_user_can_opt_in(self):

        xml = f"From=%2B123456789&Body=Hi!"

        response = self.client.post(
            self.webhook_survey_url,
            data=xml,
            content_type=self.content_type,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(SURVEY__CONFIRM_START_RESPONSE, str(response.content))

    def test_no_available_surveys(self):
        self.survey_user.completed = True
        self.survey_user.save()

        session = self.client.session
        session["survey_step"] = None
        session.save()

        xml = f"From=%2B123456789&Body={SURVEY__USER_CONFIRM_SURVEY}!"

        response = self.client.post(
            self.webhook_survey_url,
            data=xml,
            content_type=self.content_type,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(SURVEY__NO_SURVEY_AVAILABLE_RESPONSE, str(response.content))

    def test_start_survey(self):

        session = self.client.session
        session["survey_step"] = 0
        session.save()

        xml = f"From=%2B123456789&Body={SURVEY__USER_CONFIRM_SURVEY}"

        response = self.client.post(
            self.webhook_survey_url,
            data=xml,
            content_type=self.content_type,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.question_1.text, str(response.content))

    def test_no_survey_sent(self):

        session = self.client.session
        session["survey_step"] = 0
        session.save()

        xml = "From=%2B123456789&Body=No"

        response = self.client.post(
            self.webhook_survey_url,
            data=xml,
            content_type=self.content_type,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(SURVEY__CONFIRM_DO_NOT_SEND_RESPONSE, str(response.content))

    def test_survey_complete(self):
        session = self.client.session
        session["survey_step"] = 3
        session.save()

        twilio_response = MessagingResponse()
        twilio_response.message("Survey complete.")

        xml = "From=%2B123456789&Body=Response to last question asked."

        response = self.client.post(
            self.webhook_survey_url,
            data=xml,
            content_type=self.content_type,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(SURVEY__COMPLETE_RESPONSE, str(response.content))
        self.assertEqual(UserResponse.objects.count(), 1)

    def test_user_can_opt_out(self):
        session = self.client.session
        session["survey_step"] = 0
        session.save()

        xml = f"From=%2B123456789&Body={TWILIO__OPT_OUT}"

        response = self.client.post(
            self.webhook_survey_url,
            data=xml,
            content_type=self.content_type,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(SURVEY__OPT_OUT_RESPONSE, str(response.content))
