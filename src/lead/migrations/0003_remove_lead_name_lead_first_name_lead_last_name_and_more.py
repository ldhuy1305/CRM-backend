# Generated by Django 5.1.7 on 2025-03-18 08:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("lead", "0002_alter_lead_avatar"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="lead",
            name="name",
        ),
        migrations.AddField(
            model_name="lead",
            name="first_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="lead",
            name="last_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="lead",
            name="street",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
