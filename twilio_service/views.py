import traceback
from urllib.parse import parse_qs
from typing import List, Optional

from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from twilio.twiml.messaging_response import MessagingResponse
from accounts.models import UserProfile

from surveys.models import Question, SurveyUser, UserResponse
from twilio_service.constant import (
    SURVEY__COMPLETE,
    SURVEY__NO_SURVEY_SENT,
    SURVEY__START,
)

class TwilioWebhook(APIView):
    def post(self, request, *args, **kwargs):
        try:
            twilio_data = parse_qs(request.body.decode("utf-8"))
            incoming_msg_list: List[str] = twilio_data.get("Body", [])
            incoming_msg: str = " ".join(incoming_msg_list)

            phone_number_list: List[str] = twilio_data.get("From", [])
            phone_number: str = " ".join(phone_number_list)

            survey_step: int = request.session.get("survey_step", -1)
            answers: List[str] = request.session.get("answers", [])

            questions: List[Question] = (
                Question.objects.filter(survey_id=1).order_by("order")
            )

            if survey_step == -1:
                response: str = SURVEY__START
                self.initialize_survey(request)
            elif survey_step < len(questions):
                if survey_step == 0 and incoming_msg.lower() != "yes":
                    response: str = SURVEY__NO_SURVEY_SENT
                    self.reset_survey(request)
                else:
                    response: str = self.process_survey_step(
                        request, survey_step, questions, phone_number, incoming_msg
                    )
            else:
                response: str = self.finalize_survey(
                    request, survey_step, questions, phone_number, incoming_msg
                )

            twilio_response = MessagingResponse()
            twilio_response.message(response)
            twilio_response_str: str = str(twilio_response)

            return HttpResponse(twilio_response_str, content_type="application/xml")
        except Exception as e:
            traceback.print_exc()
            return JsonResponse(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def initialize_survey(self, request) -> None:
        request.session["survey_step"] = 0
        request.session["answers"] = []

    def reset_survey(self, request) -> None:
        del request.session["survey_step"]
        del request.session["answers"]

    def process_survey_step(
        self,
        request,
        survey_step: int,
        questions: List[Question],
        phone_number: str,
        incoming_msg: str,
    ) -> str:
        response: str = f"({survey_step + 1}/{len(questions)}) {questions[survey_step]}"
        self.save_user_response(questions[survey_step - 1], phone_number, incoming_msg
        )
        request.session["survey_step"] += 1
        return response

    def finalize_survey(
        self,
        request,
        survey_step: int,
        questions: List[Question],
        phone_number: str,
        incoming_msg: str,
    ) -> str:
        response: str = SURVEY__COMPLETE
        self.save_user_response(questions[survey_step - 1], phone_number, incoming_msg
        )
        del request.session["survey_step"]
        del request.session["answers"]
        return response

    def save_user_response(
        self,
        question: Question,
        phone_number: str,
        incoming_msg: str,
    ) -> None:
        last_answered_question: Question = question
        user_profile: Optional[UserProfile] = UserProfile.objects.filter(
            phone_number=phone_number
        ).first()
        if user_profile:
            UserResponse.objects.create(
                respondent=user_profile.user,
                question=last_answered_question,
                response=incoming_msg,
            ).save()
