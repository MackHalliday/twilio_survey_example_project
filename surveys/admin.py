from django.contrib import admin

from .models import Question, Survey, UserSurveySubscription, UserResponse

admin.site.register(Survey)
admin.site.register(UserSurveySubscription)
admin.site.register(Question)
admin.site.register(UserResponse)
