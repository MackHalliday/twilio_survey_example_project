from django.contrib.auth.models import User
from django.test import Client, TestCase

from accounts.models import UserProfile

# from django.urls import reverse

# from surveys.models import Question, Survey, SurveyUser
# from twilio_service.constant import TWILIO__OPT_OUT


class OptOutTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.user_profile = UserProfile.objects.create(
            user=self.user, phone_number="+123456789"
        )
        self.user_phone_number = self.user_profile.phone_number

        self.client = Client()
        self.content_type = "application/xml"

    def test_user_can_opt_out(self):
        # TODO - create class to handle user opt-out
        pass
