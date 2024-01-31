from surveys.models import Question, SurveyUser, UserResponse
from twilio_service.constant import (
    SURVEY__COMPLETE_RESPONSE,
    SURVEY__CONFIRM_DO_NOT_SEND_RESPONSE,
    SURVEY__CONFIRM_START_RESPONSE,
    SURVEY__NO_SURVEY_AVAILABLE_RESPONSE,
    SURVEY__USER_CONFIRM_SURVEY,
)


class GenerateSurveyResponse:

    def get_reponse(self, request, user, user_message):

        user_current_survey = (
            SurveyUser.objects.filter(user=user, completed=False)
            .order_by("sent_at")
            .first()
        )

        if user_current_survey is None:
            response = SURVEY__NO_SURVEY_AVAILABLE_RESPONSE

        else:
            survey_step = request.session.get("survey_step", None)

            if survey_step is None:
                response = SURVEY__CONFIRM_START_RESPONSE
                request.session["survey_step"] = 0

            elif (
                survey_step == 0 and user_message.lower() != SURVEY__USER_CONFIRM_SURVEY
            ):
                response = SURVEY__CONFIRM_DO_NOT_SEND_RESPONSE
                del request.session["survey_step"]

            else:
                questions = Question.objects.filter(
                    survey_id=user_current_survey.id
                ).order_by("order")

                total_questions = len(questions)

                if survey_step > 0:
                    last_answered_question = questions[survey_step - 1]

                    UserResponse.objects.create(
                        respondent=user,
                        question=last_answered_question,
                        response=user_message,
                    ).save()

                if survey_step < total_questions:
                    next_question = questions[survey_step].text
                    response = f"({survey_step + 1}/{total_questions}) {next_question}"

                    request.session["survey_step"] += 1
                else:
                    user_current_survey.completed = True
                    user_current_survey.save()

                    response = SURVEY__COMPLETE_RESPONSE
                    del request.session["survey_step"]

        return response
