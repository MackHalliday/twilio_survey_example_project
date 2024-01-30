
from django.db import models
from django.conf import settings


class Survey(models.Model):
    survey_name = models.TextField(null=True, blank=True)
    version = models.IntegerField(null=True,  blank=True)
    description = models.TextField(null=True,  blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Question(models.Model):
    survey = models.ForeignKey(Survey, related_name='questions', on_delete=models.CASCADE)
    order = models.PositiveIntegerField(null=True,  blank=True)
    text = models.TextField(null=True,  blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_unique_order(self):
        max_order = self.get_questions_for_survey_qs.aggregate(models.Max('order'))['order__max']
        if max_order is None:
            self.order = 1
        else:
            self.order = max_order + 1
        
    def save(self, *args, **kwargs):
        if not self.order:
            self.set_unique_order()
        super().save(*args, **kwargs)

    
    def get_questions_for_survey_qs(self):
        return Question.objects.filter(survey=self.survey)

    
    class Meta:
        unique_together = ('survey', 'order')

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    respondent = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    text = models.TextField(null=True,  blank=True)
    created_at = models.DateTimeField(auto_now_add=True)