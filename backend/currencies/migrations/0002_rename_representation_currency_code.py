# Generated by Django 4.2.1 on 2023-05-15 21:58

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("currencies", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="currency",
            old_name="representation",
            new_name="code",
        ),
    ]
