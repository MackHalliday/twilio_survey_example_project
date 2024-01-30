from django.conf import settings
from django.db import models


class Survey(models.Model):
    survey_name = models.TextField(null=True, blank=True)
    version = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class SurveyUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    sent_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ("user", "survey")


class Question(models.Model):
    survey = models.ForeignKey(
        Survey, related_name="questions", on_delete=models.CASCADE
    )
    order = models.PositiveIntegerField(null=True, blank=True)
    text = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_unique_order(self):
        max_order = self.get_questions_by_survey_id_qs(self.survey_id).aggregate(
            models.Max("order")
        )["order__max"]
        if max_order is None:
            self.order = 1
        else:
            self.order = max_order + 1

    def save(self, *args, **kwargs):
        if not self.order:
            self.set_unique_order()
        super().save(*args, **kwargs)

    def get_questions_by_survey_id_qs(self, survey_id):
        return Question.objects.filter(survey=survey_id)

    class Meta:
        unique_together = ("survey", "order")


class UserResponse(models.Model):
    question = models.ForeignKey(
        Question, related_name="answers", on_delete=models.CASCADE
    )
    respondent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    response = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
