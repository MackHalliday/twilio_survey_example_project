from django.contrib import admin

from .models import Question, Survey, SurveyUser, UserResponse

admin.site.register(Survey)
admin.site.register(SurveyUser)
admin.site.register(Question)
admin.site.register(UserResponse)
