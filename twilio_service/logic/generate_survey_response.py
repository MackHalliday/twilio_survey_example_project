from surveys.models import Question, SurveyUser, UserResponse
from twilio_service.constant import (
    SURVEY__COMPLETE,
    SURVEY__CONFIRM_START,
    SURVEY__DO_NOT_SEND_SURVEY,
    SURVEY__USER_CONFIRM_SURVEY,
)


class GenerateSurveyResponse:

    def get_reponse(self, request, user, user_message):
        survey_step = request.session.get("survey_step", None)

        user_current_survey = SurveyUser.objects.filter(
            user=user, completed=False
        ).order_by("sent_at")[0]

        questions = Question.objects.filter(survey_id=user_current_survey.id).order_by(
            "order"
        )

        if survey_step is None:
            response = SURVEY__CONFIRM_START
            request.session["survey_step"] = 0

        elif survey_step == 0 and user_message.lower() != SURVEY__USER_CONFIRM_SURVEY:
            response = SURVEY__DO_NOT_SEND_SURVEY
            del request.session["survey_step"]

        else:
            if survey_step > 0:
                last_answered_question = questions[survey_step - 1]
                UserResponse.objects.create(
                    respondent=user,
                    question=last_answered_question,
                    response=user_message,
                ).save()

            if survey_step < len(questions):
                response = f"({survey_step + 1}/{len(questions)}) {questions[survey_step].text}"
                request.session["survey_step"] += 1

            else:
                user_current_survey.completed = True
                user_current_survey.save()
                response = SURVEY__COMPLETE
                del request.session["survey_step"]

        return response
