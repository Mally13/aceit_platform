#!/usr/bin/env python3
from django_filters import rest_framework as filters
from .models import Test


class TestFilter(filters.FilterSet):
    subject_name = filters.CharFilter(field_name='subject__subject_name')
    grade = filters.CharFilter(field_name='subject__grade')
    education_level = filters.CharFilter(field_name='subject__education_level')
    pathway = filters.CharFilter(field_name='subject__pathway')
    track = filters.CharFilter(field_name='subject__track')
    class Meta:
        model = Test
        fields = ['term', 'subject_name', 'is_ready', 'created_by', 'grade',
                  'education_level', 'pathway', 'track']
