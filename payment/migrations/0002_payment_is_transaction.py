# Generated by Django 5.1.1 on 2024-11-10 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="is_transaction",
            field=models.BooleanField(default=False),
        ),
    ]
