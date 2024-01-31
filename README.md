# Project Overview 

🚧 MVP in Progress 🚧:

Small application using Django and Twilio to conduct surveys.

## Milestones
- ✅ **V0**: Basic Project Setup - Establish the foundational structure
- ✅ **V1**: Basic Models - Create basic database structure
- ✅ **V2**: Can Receive Messages - Create Twilio service to receive message
- ✅ **V3**: Can Send Message - Create Twilio service to send message
- ✅ **V4**: Iterate Twilio Service to Send Survey - Update Twilio services to send survey, waiting for response before sending the next questions.
- ✅ **V5**: Save Survey Responses - Properly save survey responses
- 🔨 **V6**: Setup AsyncWebsocket - See `/twilio_service/consumers.py`
- **V7**: Opt-In Opt-Out Service - Move service into own class
- **V8**: Setup Demo - Currently using ngrok, is there a better solution?
- **V9**: Survey campaigns - A group of users can be send a survey
- **V10**: Frontend to Setup Basic Survey - Create Admin frontend to create surveys and send
- **V11**: View Responses - Create Admin frontend to view survey response

## Tech Overview 
- **Frameworks**: Django, DjangoREST framework
- **Database**: PostgreSQL
- **Testing**: Unittest
- **Environment**: Virtual Env, DotEnv
- **Typing**: Python Typing
- **Messaging**: Twilio
- **Hosting**: Ngrok

## Resources Used 
- **[Ngrok - PIP Package Docs](https://pypi.org/project/ngrok/)**:  Reverse proxy 
- **[Ngrok - What is Ngrok](https://www.youtube.com/watch?v=UaxqJUXqvro&t=54s)**: Explainer video
- **[Twilio - Docs](https://www.twilio.com/docs/messaging)**
- **[Twilio - Send Automated Surveys by SMS](https://www.twilio.com/en-us/blog/send-automated-surveys-sms-python-twilio)**: Example by Twilio
- **[Twilio-Python Github](https://github.com/twilio/twilio-python?tab=readme-ov-file)**: Github with Twilio-Python examples
- **[Twilio-Python Python Library](https://twilio.com/docs/libraries/reference/twilio-python/)**: Docs for Twilio-Python library
