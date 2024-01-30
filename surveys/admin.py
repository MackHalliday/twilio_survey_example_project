from django.contrib import admin

from .models import Question, Survey, UserResponse

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(UserResponse)
