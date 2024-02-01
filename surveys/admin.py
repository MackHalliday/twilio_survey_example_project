from django.contrib import admin

from .models import Question, Survey, UserResponse, UserSurveySubscription

admin.site.register(Survey)
admin.site.register(UserSurveySubscription)
admin.site.register(Question)
admin.site.register(UserResponse)
