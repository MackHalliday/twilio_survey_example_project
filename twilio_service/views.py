# twilio_service/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
import json
from typing import Any
from urllib.parse import parse_qs

from surveys.models import Question
import traceback


# from django.contrib.auth.models import User

# from surveys.models import Question, UserResponse

class TwilioWebhook(APIView):
    def post(self, request: Any, *args: Any, **kwargs: Any) -> Any:
        try:
            twilio_data = parse_qs(request.body.decode("utf-8"))

            incoming_msg: str = twilio_data.get('Body', '')
            # phone_number: str = twilio_data.get("From")
            survey_step: int = twilio_data.get('survey_step', -1)

            questions = Question.objects.filter(survey_id=1).values_list('text', flat=True)

            if survey_step == -1:
                response = "Hello!"
                request.session['survey_step'] = 0
                request.session['answers'] = []
            elif survey_step < len(questions):
                if survey_step == 0 and incoming_msg.lower() != 'yes':
                    response = "Let's go!"
                    del request.session['survey_step']
                    del request.session['answers']
                else:
                    response = f'({survey_step + 1}/{len(questions)}) {questions[survey_step]}'
                    request.session['survey_step'] += 1
                    if survey_step > 0:
                        request.session['answers'].append(incoming_msg)
            else:
                response = "EXIT"
                answers = request.session['answers']
                answers.append(incoming_msg)
                del request.session['survey_step']
                del request.session['answers']
                print('Survey answers:', answers)

            # user = User.objects.filter(phone_number=phone_number, is_active=True).first()
            # current_survey_campaign = SurveyCampaign.object.filter(user, is_active=True)
            # question = Question.objects.filter(survey=current_survey_campaign.survey_id)

            # user_response = UserResponse.objects.create(respondent=user, question=question, response=message_body)

            # if not user_survey_complete(user): 
            #     send_user_next_survey_question(user)

            return Response(data={"response":response}, status=status.HTTP_200_OK)
        except Exception as e:
            traceback.print_exc()
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
