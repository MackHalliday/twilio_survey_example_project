# Generated by Django 5.0.1 on 2024-01-30 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_alter_userprofile_phone_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="id",
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
