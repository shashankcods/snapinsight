# Generated by Django 5.1.5 on 2025-02-07 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photoapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='photo',
            name='brightness_score',
        ),
        migrations.RemoveField(
            model_name='photo',
            name='sharpness_score',
        ),
        migrations.AddField(
            model_name='photo',
            name='blacks_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='exposure_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='highlights_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='shadows_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='temperature_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='tint_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='vibrance_score',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='photo',
            name='whites_score',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
