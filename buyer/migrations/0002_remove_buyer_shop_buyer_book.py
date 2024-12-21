# Generated by Django 5.1.1 on 2024-11-04 08:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("buyer", "0001_initial"),
        ("seller", "0003_remove_cart_item_remove_cart_user_delete_cartbooks_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="buyer",
            name="shop",
        ),
        migrations.AddField(
            model_name="buyer",
            name="book",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="seller.book",
            ),
        ),
    ]
