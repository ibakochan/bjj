# Generated by Django 4.2.3 on 2023-10-30 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0029_alter_lesson_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="participationcount",
            name="monthly_count_b",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="participationcount",
            name="monthly_count_c",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="participationcount",
            name="monthly_count_f",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="participationcount",
            name="monthly_count_j",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
