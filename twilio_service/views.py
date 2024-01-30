# twilio_service/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import json
from typing import Any
from urllib.parse import parse_qs

# from django.contrib.auth.models import User

# from surveys.models import Question, UserResponse

class TwilioWebhook(APIView):
    def post(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            twilio_data = parse_qs(request.body.decode("utf-8"))
            
            phone_number = twilio_data.get("From")
            message_body = twilio_data.get("Body")

            # user = User.objects.filter(phone_number=phone_number, is_active=True).first()
            # current_survey_campaign = SurveyCampaign.object.filter(user, is_active=True)
            # question = Question.objects.filter(survey=current_survey_campaign.survey_id)

            # user_response = UserResponse.objects.create(respondent=user, question=question, response=message_body)

            # if not user_survey_complete(user): 
            #     send_user_next_survey_question(user)

            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
