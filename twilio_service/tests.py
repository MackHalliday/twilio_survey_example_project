from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
import phonenumbers
from twilio.twiml.messaging_response import MessagingResponse

from accounts.models import UserProfile
from surveys.models import Question, Survey, SurveyUser, UserResponse
from twilio_service.constant import (
    SURVEY__COMPLETE,
    SURVEY__DO_NOT_SEND_SURVEY,
    SURVEY__USER_CONFIRM_SURVEY,
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

        self.survey_user = SurveyUser.objects.create(
            survey=self.survey, user=self.user, completed=False
        )

        self.client = Client()
        self.content_type = "application/xml"

    def test_start_survey(self):

        session = self.client.session
        session["survey_step"] = 1
        session.save()

        xml = f"From=%2B123456789&Body={SURVEY__USER_CONFIRM_SURVEY}s"

        response = self.client.post(
            reverse("income-message"),
            data=xml,
            content_type=self.content_type,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.question_1.text, str(response.content))

    def test_no_survey_sent(self):

        session = self.client.session
        session["survey_step"] = None
        session.save()

        xml = "From=%2B123456789&Body=No"

        response = self.client.post(
            reverse("income-message"),
            data=xml,
            content_type=self.content_type,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(SURVEY__DO_NOT_SEND_SURVEY, str(response.content))

    def test_survey_complete(self):
        session = self.client.session
        session["survey_step"] = 4
        session.save()

        twilio_response = MessagingResponse()
        twilio_response.message("Survey complete.")

        xml = "From=%2B123456789&Body=Response to last question asked."

        response = self.client.post(
            reverse("income-message"),
            data=xml,
            content_type=self.content_type,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(SURVEY__COMPLETE, str(response.content))
        self.assertEqual(UserResponse.objects.count(), 1)

    def test_user_opt_out(self): 
        pass