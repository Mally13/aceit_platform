# Generated by Django 5.0.6 on 2024-07-02 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_subject_subject_unique_subject'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subject',
            name='pathway',
            field=models.CharField(blank=True, choices=[('arts_sport_science', 'Arts and Sport Science'), ('social_sciences', 'Social Sciences'), ('stem', 'Science Technology Engineering and Mathematics (STEM)')], default='N/A', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='subject',
            name='track',
            field=models.CharField(blank=True, choices=[('arts', 'Arts'), ('sports_science', 'Sports Science'), ('humanities', 'Humanities'), ('languages', 'Languages'), ('business_studies', 'Business Studies'), ('pure_sciences', 'Pure Sciences'), ('applied_sciences', 'Applied Sciences'), ('technical_engineering', 'Technical and Engineering'), ('career_technology', 'Career and Technology Studies')], default='N/A', max_length=50, null=True),
        ),
    ]
