import traceback
from urllib.parse import parse_qs

from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from twilio.twiml.messaging_response import MessagingResponse

from surveys.models import Question


class TwilioWebhook(APIView):
    def post(self, request, *args, **kwargs):
        try:
            twilio_data = parse_qs(request.body.decode("utf-8"))

            incoming_msg = twilio_data.get("Body", "")
            survey_step = twilio_data.get("survey_step", -1)

            questions = Question.objects.filter(survey_id=1).values_list(
                "text", flat=True
            )

            # TODO - Sessions NOT working correctly
            if survey_step == -1:
                response = "Hello!"
                request.session["survey_step"] = 0
                request.session["answers"] = []
            elif survey_step < len(questions):
                if survey_step == 0 and incoming_msg.lower() != "yes":
                    response = "Let's go!"
                    del request.session["survey_step"]
                    del request.session["answers"]
                else:
                    response = (
                        f"({survey_step + 1}/{len(questions)}) {questions[survey_step]}"
                    )
                    request.session["survey_step"] += 1
                    if survey_step > 0:
                        request.session["answers"].append(incoming_msg)
            else:
                response = "EXIT"
                answers = request.session["answers"]
                answers.append(incoming_msg)
                del request.session["survey_step"]
                del request.session["answers"]
                print("Survey answers:", answers)

            # user = User.objects.filter(phone_number=phone_number, is_active=True).first()
            # current_survey_campaign = SurveyCampaign.object.filter(user, is_active=True)
            # question = Question.objects.filter(survey=current_survey_campaign.survey_id)

            # user_response = UserResponse.objects.create(respondent=user, question=question, response=message_body)

            # if not user_survey_complete(user):
            #     send_user_next_survey_question(user)

            # return Response(data={"response":response}, status=status.HTTP_200_OK)

            twilio_response = MessagingResponse()
            twilio_response.message(response)
            twilio_response_str = str(twilio_response)

            return HttpResponse(twilio_response_str, content_type="application/xml")
        except Exception as e:
            traceback.print_exc()
            return JsonResponse(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
