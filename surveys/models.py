from django.conf import settings
from django.db import models


class Survey(models.Model):
    id = models.AutoField(primary_key=True)
    survey_name = models.TextField(null=True, blank=True)
    version = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class UserSurveySubscription(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)

    @classmethod
    def get_current_survey_for_user(cls, user):
        return cls.objects.filter(user=user, completed=False).order_by("sent_at")

    class Meta:
        unique_together = ("user", "survey")

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    survey = models.ForeignKey(
        Survey, related_name="questions", on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_questions_by_survey_qs(cls, survey_id):
        return cls.objects.filter(survey_id=survey_id).order_by("order")

    def set_unique_order(self):
        max_order = self.get_questions_by_survey_qs(self.survey)[-1].order
        self.order = 1 if None else max_order + 1

    def save(self, *args, **kwargs):
        if not self.order:
            self.set_unique_order()
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ("survey", "order")


class UserResponse(models.Model):
    id = models.AutoField(primary_key=True)
    question = models.ForeignKey(
        Question, related_name="answers", on_delete=models.CASCADE
    )
    respondent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    response = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def save_user_response(cls, respondent, question, response):
        return cls.objects.create(respondent=respondent, question=question, response=response)