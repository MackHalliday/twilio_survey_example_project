from surveys.models import Question, UserResponse, UserSurveySubscription
from twilio_service.constant import (
    SURVEY__COMPLETE_RESPONSE,
    SURVEY__CONFIRM_DO_NOT_SEND_RESPONSE,
    SURVEY__CONFIRM_START_RESPONSE,
    SURVEY__NO_SURVEY_AVAILABLE_RESPONSE,
    SURVEY__OPT_IN_RESPONSE,
    SURVEY__OPT_OUT_RESPONSE,
    SURVEY__PREVIOUSLY_SUBSCRIBED,
    SURVEY__USER_CONFIRM_SURVEY,
    TWILIO__OPT_OUT,
)


class SurveyResponseService:
    def __init__(self, request, user, user_response):
        self.request = request
        self.user = user 
        self.user_response = user_response

    def get_subscription_status(self, user_profile):
        
        if not user_profile.active:
            return SURVEY__PREVIOUSLY_SUBSCRIBED
    
        elif self.user_response.lower() == TWILIO__OPT_OUT:
            user_profile.active = False
            user_profile.save()
            self.request.session.pop("survey_step", None)
            return SURVEY__OPT_OUT_RESPONSE
            
        elif self.user_message.lower() == TWILIO__OPT_OUT:
            user_profile.active = True
            user_profile.save()
            return SURVEY__OPT_IN_RESPONSE
    
    

    def get_reponse(self):

        current_subscription = UserSurveySubscription.get_current_survey_subscription(
            self.user
        )

        if not current_subscription:
            twilio_response = SURVEY__NO_SURVEY_AVAILABLE_RESPONSE

        else:
            survey = current_subscription[0].survey
            survey_step = self.request.session.get("survey_step", None)

            if survey_step is None:
                self.request.session["survey_step"] = 0
                return SURVEY__CONFIRM_START_RESPONSE

            if (
                survey_step == 0
                and self.user_response.lower() != SURVEY__USER_CONFIRM_SURVEY
            ):
                
                del self.request.session["survey_step"]
                return SURVEY__CONFIRM_DO_NOT_SEND_RESPONSE

            
            questions = Question.get_questions_by_survey_qs(survey)
            total_questions = len(questions)

            if survey_step > 0:
                previous_question = questions[survey_step - 1]

                UserResponse.save_user_response(
                    self.user, previous_question, self.user_response
                )

            if survey_step < total_questions:
                next_question = questions[survey_step].text
                twilio_response = (
                    f"({survey_step + 1}/{total_questions}) {next_question}"
                )

                self.request.session["survey_step"] += 1
                
            else:
                survey.completed = True
                survey.save()

                twilio_response = SURVEY__COMPLETE_RESPONSE
                del self.request.session["survey_step"]

        return twilio_response
