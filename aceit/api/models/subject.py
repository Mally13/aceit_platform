#!/usr/bin/env python3
"""
Module defines app Subject model
"""
from django.db import models


class Subject(models.Model):
    """
    Defines a Subject model.

    This model will get an id for a subject at every level, grade, pathway
    and track(if exists)
    """
    EDUCATION_LEVEL_CHOICES = (
        ('pre_primary', 'Pre-Primary'),
        ('lower_primary', 'Lower Primary'),
        ('upper_primary', 'Upper Primary'),
        ('junior_secondary', 'Junior Secondary'),
        ('senior_secondary', 'Senior Secondary'),
    )

    PATHWAY_CHOICES = (
        ('N/A', 'N/A'),
        ('arts_sport_science', 'Arts and Sport Science'),
        ('social_sciences', 'Social Sciences'),
        ('stem', 'Science Technology Engineering and Mathematics (STEM)'),
    )

    TRACK_CHOICES = [
        ('N/A', 'N/A'),
        ('arts', 'Arts'),
        ('sports_science', 'Sports Science'),
        ('humanities', 'Humanities'),
        ('languages', 'Languages'),
        ('business_studies', 'Business Studies'),
        ('pure_sciences', 'Pure Sciences'),
        ('applied_sciences', 'Applied Sciences'),
        ('technical_engineering', 'Technical and Engineering'),
        ('career_technology', 'Career and Technology Studies'),
    ]

    GRADE_CHOICES = (
        ('pp1', 'PP1'),
        ('pp2', 'PP2'),
        ('1', 'Grade 1'),
        ('2', 'Grade 2'),
        ('3', 'Grade 3'),
        ('4', 'Grade 4'),
        ('5', 'Grade 5'),
        ('6', 'Grade 6'),
        ('7', 'Grade 7'),
        ('8', 'Grade 8'),
        ('9', 'Grade 9'),
        ('10', 'Grade 10'),
        ('11', 'Grade 11'),
        ('12', 'Grade 12'),
    )

    subject_name = models.CharField(max_length=50)
    education_level = models.CharField(max_length=50, choices=EDUCATION_LEVEL_CHOICES)
    pathway = models.CharField(max_length=50, choices=PATHWAY_CHOICES)
    track = models.CharField(max_length=50, choices=TRACK_CHOICES)
    grade = models.CharField(max_length=10, choices=GRADE_CHOICES)

    class Meta:
        """
        Defines constraint to ensure that a subject entry is not repeated.
        """
        unique_together = ['subject_name', 'education_level', 'pathway', 'track', 'grade']

    def __str__(self):
        """
        Returns a string representation of the object.

        This method returns a string representation of the Subject object.
        """
        return f'{self.subject_name} Grade {self.grade}'
