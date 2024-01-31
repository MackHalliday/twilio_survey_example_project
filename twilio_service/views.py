import traceback
from urllib.parse import parse_qs

from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from twilio.twiml.messaging_response import MessagingResponse

from accounts.models import UserProfile
from surveys.models import Question, SurveyUser, UserResponse
from twilio_service.constant import (
    SURVEY__COMPLETE,
    SURVEY__CONFIRM_START,
    SURVEY__DO_NOT_SEND_SURVEY,
    SURVEY__OPT_OUT_MESSAGE,
    SURVEY__USER_CONFIRM_SURVEY,
    TWILIO__OPT_OUT,
)


class TwilioWebhook(APIView):
    def post(self, request, *args, **kwargs):
        try:
            # Get phone number and message from twilio data
            twilio_data = parse_qs(request.body.decode("utf-8"))

            phone_number_list = twilio_data.get("From", [])
            phone_number = " ".join(phone_number_list)

            incoming_msg_list = twilio_data.get("Body", [])
            incoming_msg = " ".join(incoming_msg_list)

            # Get user by phone number
            user_profile = UserProfile.objects.filter(
                phone_number=phone_number,
            ).first()

            # If 'opt-out' then do
            if incoming_msg == TWILIO__OPT_OUT:
                user_profile.update(active=False)
                response = SURVEY__OPT_OUT_MESSAGE
                del request.session["survey_step"]

            # Else send survey
            else:
                survey_step = request.session.get("survey_step", None)

                user_current_survey = SurveyUser.objects.filter(
                    user=user_profile.user, is_active=True
                ).order_by("sent_at")[0]
                questions = Question.objects.filter(
                    survey_id=user_current_survey
                ).order_by("order")

                if not survey_step:
                    response = SURVEY__CONFIRM_START
                    request.session["survey_step"] = 0

                elif (
                    survey_step == 0
                    and incoming_msg.lower() != SURVEY__USER_CONFIRM_SURVEY
                ):
                    response = SURVEY__DO_NOT_SEND_SURVEY
                    del request.session["survey_step"]

                else:
                    last_answered_question = questions[survey_step - 1]

                    UserResponse.objects.create(
                        respondent=user_profile.user,
                        question=last_answered_question,
                        response=incoming_msg,
                    ).save()

                    if survey_step > len(questions):
                        response = f"({survey_step + 1}/{len(questions)}) {questions[survey_step]}"
                        request.session["survey_step"] += 1

                    else:
                        response = SURVEY__COMPLETE
                        del request.session["survey_step"]

            twilio_response = MessagingResponse()
            twilio_response.message(response)
            twilio_response_str = str(twilio_response)

            return HttpResponse(twilio_response_str, content_type="application/xml")
        except Exception as e:
            traceback.print_exc()
            return JsonResponse(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
