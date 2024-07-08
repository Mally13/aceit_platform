from django.db import models
from django.conf import settings
from .category import Category


class Test(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('complete', 'Complete'),
    ]

    TERM_CHOICES = [
        ('1', 'Term 1'),
        ('2', 'Term 2'),
        ('3', 'Term 3'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    display_picture = models.ImageField(
        upload_to='test_display_pictures/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    duration = models.DurationField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    term = models.CharField(
        max_length=5, choices=TERM_CHOICES, null=True, blank=True)
    status = models.CharField(
        max_length=8, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return self.title
