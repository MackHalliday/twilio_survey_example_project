from surveys.models import Question, SurveyUser, UserResponse
from twilio_service.constant import (
    SURVEY__COMPLETE_RESPONSE,
    SURVEY__CONFIRM_DO_NOT_SEND_RESPONSE,
    SURVEY__CONFIRM_START_RESPONSE,
    SURVEY__NO_SURVEY_AVAILABLE_RESPONSE,
    SURVEY__USER_CONFIRM_SURVEY,
)


class GenerateSurveyResponse:

    def get_reponse(self, request, user, user_response):

        user_current_survey = SurveyUser.get_(user)

        if user_current_survey is None:
            twilio_response = SURVEY__NO_SURVEY_AVAILABLE_RESPONSE

        else:
            survey_step = request.session.get("survey_step", None)

            if survey_step is None:
                twilio_response = SURVEY__CONFIRM_START_RESPONSE
                request.session["survey_step"] = 0

            elif (
                survey_step == 0 and user_response.lower() != SURVEY__USER_CONFIRM_SURVEY
            ):
                twilio_response = SURVEY__CONFIRM_DO_NOT_SEND_RESPONSE
                del request.session["survey_step"]

            else:
                questions = Question.get_questions_by_survey_qs(user_current_survey)
                total_questions = len(questions)

                if survey_step > 0:
                    previous_question = questions[survey_step - 1]

                    UserResponse.save_user_response(user, previous_question, user_response)

                if survey_step < total_questions:
                    next_question = questions[survey_step].text
                    twilio_response  = f"({survey_step + 1}/{total_questions}) {next_question}"

                    request.session["survey_step"] += 1
                else:
                    user_current_survey.completed = True
                    user_current_survey.save()

                    twilio_response = SURVEY__COMPLETE_RESPONSE
                    del request.session["survey_step"]

        return twilio_response
