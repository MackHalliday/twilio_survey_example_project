import traceback
from urllib.parse import parse_qs

from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from twilio.twiml.messaging_response import MessagingResponse

from accounts.models import UserProfile
from surveys.models import Question, SurveyUser, UserResponse
from twilio_service.constant import SURVEY__OPT_OUT_RESPONSE, TWILIO__OPT_OUT
from twilio_service.logic.generate_survey_response import GenerateSurveyResponse


class TwilioWebhook(APIView):
    def post(self, request, *args, **kwargs):
        try:
            twilio_data = parse_qs(request.body.decode("utf-8"))

            phone_number = " ".join(twilio_data.get("From", []))
            user_message = " ".join(twilio_data.get("Body", []))

            user_profile = UserProfile.objects.get(phone_number=phone_number)
            user = user_profile.user

            if user_message.lower() == TWILIO__OPT_OUT:
                user_profile.active = False
                user_profile.save()

                response = SURVEY__OPT_OUT_RESPONSE
                del request.session["survey_step"]

            else:
                response = GenerateSurveyResponse.get_reponse(
                    self, request, user, user_message
                )

            twilio_response = MessagingResponse()
            twilio_response.message(response)
            twilio_response_str = str(twilio_response)

            return HttpResponse(twilio_response_str, content_type="application/xml")

        except Exception as e:
            traceback.print_exc()

            return JsonResponse(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
