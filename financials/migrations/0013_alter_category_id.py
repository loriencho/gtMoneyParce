# Generated by Django 4.2.20 on 2025-04-27 17:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("financials", "0012_delete_budget"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
