from django.db import models
from .test import Test

class Question(models.Model):
    test = models.ForeignKey(Test, on_delete=models.CASCADE, related_name='questions')
    images = models.ImageField(upload_to='question_images/', blank=True, null=True)
    question_text = models.TextField()
    options = models.JSONField()
    correct_answer = models.CharField(max_length=255)
    explanation = models.TextField()
    reveal_answer_after_completion = models.BooleanField(default=False)
    reveal_explanation_after_completion = models.BooleanField(default=False)

    def __str__(self):
        return f"Question {self.id} for {self.test.title}"