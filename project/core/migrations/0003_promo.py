# Generated by Django 4.1 on 2022-09-28 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_alter_movie_options_movie_pic_movie_release_date_and_more")
    ]

    operations = [
        migrations.CreateModel(
            name="Promo",
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
                ("name", models.CharField(max_length=200)),
                ("code", models.CharField(max_length=6)),
            ],
        )
    ]