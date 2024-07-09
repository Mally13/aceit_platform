#!/usr/bin/env python3
"""
Module defines apps Category model
"""
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    """Defines the category model of the app"""
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    level = models.IntegerField(default=0)
    rght = models.IntegerField(default=0) 

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name
