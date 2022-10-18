# Generated by Django 4.1 on 2022-10-18 05:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("core", "0008_alter_promo_code_alter_promo_exp_date")]

    operations = [
        migrations.AlterField(
            model_name="promo",
            name="code",
            field=models.CharField(default="378B5M", max_length=6),
        ),
        migrations.AlterField(
            model_name="promo",
            name="exp_date",
            field=models.DateField(
                default=datetime.datetime(2022, 11, 17, 1, 2, 4, 228690)
            ),
        ),
    ]
