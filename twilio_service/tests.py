from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from twilio.twiml.messaging_response import MessagingResponse

from accounts.models import UserProfile
from surveys.models import Question, Survey, UserResponse


class TwilioWebhookTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.survey = Survey.objects.create(survey_name="Test Survey", version=1)

    @patch("twilio_service.views.parse_qs")
    def test_start_survey(self, mock_parse_qs):
        mock_parse_qs.return_value = {"Body": ["yes"], "From": ["+1234567890"]}
        twilio_response = MessagingResponse()
        twilio_response.message("Hello!")

        with patch.object(
            MessagingResponse, "__str__", return_value=str(twilio_response)
        ):
            response = self.client.post(
                reverse("income-message"),
                data={
                    "Body": "Yes",
                    "From": "+1234567890",
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Hello!", str(response.content))

    @patch("twilio_service.views.parse_qs")
    def test_no_survey_sent(self, mock_parse_qs):
        mock_parse_qs.return_value = {"Body": ["no"], "From": ["+1234567890"]}
        twilio_response = MessagingResponse()
        twilio_response.message("No survey sent.")

        with patch.object(
            MessagingResponse, "__str__", return_value=str(twilio_response)
        ):
            response = self.client.post(
                reverse("income-message"),
                data={
                    "Body": "no",
                    "From": "+1234567890",
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn("No survey sent.", str(response.content))

    @patch("twilio_service.views.parse_qs")
    def test_survey_complete(self, mock_parse_qs):
        mock_parse_qs.return_value = {"Body": ["answer"], "From": ["+1234567890"]}
        UserProfile.objects.create(phone_number="+1234567890", user=self.user)
        Question.objects.create(survey=self.survey, text="Question 1")
        self.client.session["survey_step"] = 0

        twilio_response = MessagingResponse()
        twilio_response.message("Survey complete.")

        with patch.object(
            MessagingResponse, "__str__", return_value=str(twilio_response)
        ):
            response = self.client.post(
                reverse("income-message"),
                data={
                    "Body": "answer",
                    "From": "+1234567890",
                },
            )

        self.assertEqual(response.status_code, 200)
        self.assertIn("Survey complete.", str(response.content))
        self.assertEqual(UserResponse.objects.count(), 1)
