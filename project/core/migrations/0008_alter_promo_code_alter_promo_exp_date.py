# Generated by Django 4.1 on 2022-09-29 07:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0007_rename_tag_line_movie_tag_alter_genre_title_and_more")
    ]

    operations = [
        migrations.AlterField(
            model_name="promo",
            name="code",
            field=models.CharField(default="L4F1R8", max_length=6),
        ),
        migrations.AlterField(
            model_name="promo",
            name="exp_date",
            field=models.DateField(
                default=datetime.datetime(2022, 10, 29, 3, 39, 10, 194456)
            ),
        ),
    ]