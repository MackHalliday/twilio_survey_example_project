import traceback
from urllib.parse import parse_qs

from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from twilio.twiml.messaging_response import MessagingResponse

from surveys.models import Question, UserResponse
from twilio_service.constant import (SURVEY__COMPLETE, SURVEY__NO_SURVEY_SENT,
                                     SURVEY__START)


class TwilioWebhook(APIView):
    def post(self, request, *args, **kwargs):
        try:
            twilio_data = parse_qs(request.body.decode("utf-8"))
            incoming_msg_list = twilio_data.get("Body", [])
            incoming_msg = " ".join(incoming_msg_list)

            phone_number_list = twilio_data.get("Number", [])
            phone_number = " ".join(phone_number_list)

            survey_step = request.session.get("survey_step", -1)
            answers = request.session.get("answers", [])

            questions = Question.objects.filter(survey_id=1).values_list(
                "text", flat=True
            )

            if survey_step == -1:
                response = SURVEY__START
                request.session["survey_step"] = 0
                request.session["answers"] = []
            elif survey_step < len(questions):
                if survey_step == 0 and incoming_msg.lower() != "yes":
                    response = SURVEY__NO_SURVEY_SENT
                    del request.session["survey_step"]
                    del request.session["answers"]
                else:
                    response = (
                        f"({survey_step + 1}/{len(questions)}) {questions[survey_step]}"
                    )
                    request.session["survey_step"] += 1

                    user = User.objects.filter(
                        phone_number=phone_number, is_active=True
                    ).first()
                    current_survey_campaign = SurveyCampaign.object.filter(
                        user, is_active=True
                    )
                    question = Question.objects.filter(
                        survey=current_survey_campaign.survey_id
                    )

                    user_response = UserResponse.objects.create(
                        respondent=user, question=question, response=incoming_msg
                    )

                    if survey_step > 0:
                        answers.append(incoming_msg)
            else:
                response = SURVEY__COMPLETE
                answers.append(incoming_msg)
                del request.session["survey_step"]
                del request.session["answers"]

            twilio_response = MessagingResponse()
            twilio_response.message(response)
            twilio_response_str = str(twilio_response)

            return HttpResponse(twilio_response_str, content_type="application/xml")
        except Exception as e:
            traceback.print_exc()
            return JsonResponse(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
