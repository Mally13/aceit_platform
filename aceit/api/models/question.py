from django.db import models
from django.contrib.postgres.fields import ArrayField

from .test import Test


class Question(models.Model):
    question_text = models.TextField()
    options = ArrayField(models.TextField, blank=True, null=True)
    correct_answers = ArrayField(models.TextField)
    explanation = models.TextField()
    has_multiple_correct_answers = models.BooleanField()
    test = models.ForeignKey(
        Test, on_delete=models.CASCADE, related_name='questions')
    images = models.ImageField(
        upload_to='question_images/', blank=True, null=True)
    # reveal_answer_after_completion = models.BooleanField(default=False)
    # reveal_explanation_after_completion = models.BooleanField(default=False)

    def __str__(self):
        return f"Question {self.id} for {self.test.title}"
