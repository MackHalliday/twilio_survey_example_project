from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse
import phonenumbers
from twilio.twiml.messaging_response import MessagingResponse

from accounts.models import UserProfile
from surveys.models import Question, Survey, SurveyUser, UserResponse
from twilio_service.constant import (
    SURVEY__DO_NOT_SEND_SURVEY,
    SURVEY__USER_CONFIRM_SURVEY,
)


class TwilioWebhookTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.user_profile = UserProfile.objects.create(
            user=self.user, phone_number="+13092125377"
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

    def test_start_survey(self):

        session = self.client.session
        session["survey_step"] = 1
        session.save()

        response = self.client.post(
            reverse("income-message"),
            data={
                "Body": SURVEY__USER_CONFIRM_SURVEY,
                "From": str(self.user_phone_number),
            },
            content_type="application/x-www-form-urlencoded",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn(self.question_1.text, str(response.content))

    def test_no_survey_sent(self):

        session = self.client.session
        session["survey_step"] = None
        session.save()

        response = self.client.post(
            reverse("income-message"),
            data={"Body": "No", "From": str(self.user_phone_number)},
            content_type="application/x-www-form-urlencoded",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(SURVEY__DO_NOT_SEND_SURVEY, str(response.content))

    def test_survey_complete(self):
        session = self.client.session
        session["survey_step"] = 2
        session.save()

        twilio_response = MessagingResponse()
        twilio_response.message("Survey complete.")

        response = self.client.post(
            reverse("income-message"),
            data={
                "Body": "Last answer to question.",
                "From": str(self.user_phone_number),
            },
            content_type="application/x-www-form-urlencoded",
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Survey complete.", str(response.content))
        self.assertEqual(UserResponse.objects.count(), 1)
