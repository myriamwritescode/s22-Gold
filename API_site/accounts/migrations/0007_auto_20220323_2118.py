# Generated by Django 3.2.4 on 2022-03-23 21:18

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_customer_age_customer_city_customer_zip_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='date_created',
        ),
        migrations.AddField(
            model_name='customer',
            name='agriculture_and_food',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Agriculture and Food'),
        ),
        migrations.AddField(
            model_name='customer',
            name='armedforces_and_nationalsecurity',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Armed Forces and National Security'),
        ),
        migrations.AddField(
            model_name='customer',
            name='civilrights_and_liberties_minorityissues',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Civil Rights and Liberties, Minority Issues'),
        ),
        migrations.AddField(
            model_name='customer',
            name='crime_and_lawenforcement',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Crime and Law Enforcement'),
        ),
        migrations.AddField(
            model_name='customer',
            name='economics_and_public_finance',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Economics and Public Finance'),
        ),
        migrations.AddField(
            model_name='customer',
            name='education',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Education'),
        ),
        migrations.AddField(
            model_name='customer',
            name='emergency_management',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Emergency Management'),
        ),
        migrations.AddField(
            model_name='customer',
            name='environmental_protection',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Environmental Protection'),
        ),
        migrations.AddField(
            model_name='customer',
            name='governmentoperations_and_politics',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Government Operations and Politics'),
        ),
        migrations.AddField(
            model_name='customer',
            name='health',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Health'),
        ),
        migrations.AddField(
            model_name='customer',
            name='immigration',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Immigration'),
        ),
        migrations.AddField(
            model_name='customer',
            name='internationalaffairs',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='International Affairs'),
        ),
        migrations.AddField(
            model_name='customer',
            name='labor_and_employment',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Labor and Employment'),
        ),
        migrations.AddField(
            model_name='customer',
            name='science_technology_communications',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Science, Technology, Communications'),
        ),
        migrations.AddField(
            model_name='customer',
            name='social_welfare',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Social Welfare'),
        ),
        migrations.AddField(
            model_name='customer',
            name='taxation',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Taxation'),
        ),
        migrations.AddField(
            model_name='customer',
            name='transportation_and_public_works',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)], verbose_name='Transportation and Public Works'),
        ),
    ]
