# Generated by Django 4.1 on 2022-10-19 04:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("accounts", "0004_alter_customuser_profile_pic")]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="address",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="accounts.address",
            ),
        )
    ]