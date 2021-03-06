# Generated by Django 3.2.6 on 2021-08-06 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Listing",
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
                ("listing_id", models.IntegerField(unique=True)),
                ("name", models.CharField(max_length=255)),
                ("profile_url", models.CharField(max_length=255)),
                ("street", models.CharField(max_length=255)),
                ("zipcode", models.CharField(max_length=10)),
                ("outcode", models.CharField(max_length=10)),
                (
                    "daily_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=20
                    ),
                ),
                (
                    "weekly_price",
                    models.DecimalField(
                        decimal_places=2, max_digits=20
                    ),
                ),
            ],
            options={"db_table": "listing"},
        )
    ]
