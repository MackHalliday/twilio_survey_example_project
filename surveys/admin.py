from django.contrib import admin

from .models import Question, Survey, UserResponse, SurveyUser

admin.site.register(Survey)
admin.site.register(SurveyUser)
admin.site.register(Question)
admin.site.register(UserResponse)
