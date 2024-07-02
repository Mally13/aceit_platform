from django.db import models
from django.conf import settings
from .category import Category

class Test(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('complete', 'Complete'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title
