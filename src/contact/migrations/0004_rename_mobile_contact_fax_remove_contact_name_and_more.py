# Generated by Django 5.1.7 on 2025-03-20 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contact", "0003_contact_created_at_contact_created_by_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="contact",
            old_name="mobile",
            new_name="fax",
        ),
        migrations.RemoveField(
            model_name="contact",
            name="name",
        ),
        migrations.AddField(
            model_name="contact",
            name="city",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="contact",
            name="country",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="contact",
            name="first_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="contact",
            name="last_name",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="contact",
            name="postal_code",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name="contact",
            name="state_province",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="contact",
            name="street",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="contact",
            name="website",
            field=models.URLField(blank=True, null=True),
        ),
    ]
