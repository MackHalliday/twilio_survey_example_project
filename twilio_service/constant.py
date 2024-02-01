TWILIO__OPT_IN = "start survey"
TWILIO__OPT_OUT = "stop survey"
TWILIO__UNKNOWN_USER = "Service is unavailable."

SURVEY__USER_CONFIRM_SURVEY = "yes"
SURVEY__COMPLETE_RESPONSE = "Thank you for completing the survey!"
SURVEY__CONFIRM_START_RESPONSE = (
    f"Would you like to take a survey? Response {SURVEY__USER_CONFIRM_SURVEY.upper()} to start."
)
SURVEY__CONFIRM_DO_NOT_SEND_RESPONSE = "No survey will be sent."
SURVEY__PREVIOUSLY_SUBSCRIBED = f"You previously unsubscribed to this survey. Reply {TWILIO__OPT_IN.upper()} to resubscribe."
SURVEY__NO_SURVEY_AVAILABLE_RESPONSE = "All available surveys have been completed."
SURVEY__OPT_OUT_RESPONSE = f"You have been unsubscribed this survey. Reply {TWILIO__OPT_IN.upper()} to resubscribe."
SURVEY__OPT_IN_RESPONSE = f"You have resubscribed to this survey. Reply {TWILIO__OPT_OUT.upper()} to unsubscribe at anytime."