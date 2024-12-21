# Generated by Django 5.1.1 on 2024-11-04 01:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("seller", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="CartBooks",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("book_name", models.CharField(max_length=50)),
                ("book_discription", models.CharField(max_length=100)),
                ("book_price", models.FloatField()),
                ("book_quantity", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Cart",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="seller.cartbooks",
                    ),
                ),
            ],
        ),
    ]
