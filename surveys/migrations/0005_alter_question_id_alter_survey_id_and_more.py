# Generated by Django 5.0.1 on 2024-01-30 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("surveys", "0004_surveyuser"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="survey",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="surveyuser",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="userresponse",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
