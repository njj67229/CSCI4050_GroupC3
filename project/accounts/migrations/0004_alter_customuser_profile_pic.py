# Generated by Django 4.1 on 2022-10-19 01:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("accounts", "0003_customuser_profile_pic")]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="profile_pic",
            field=models.ImageField(
                blank=True,
                default="profiles/default_profile.jpg",
                upload_to="profiles/",
            ),
        )
    ]
