from django.contrib import admin
from .models import Survey, Question, UserResponse

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(UserResponse)
