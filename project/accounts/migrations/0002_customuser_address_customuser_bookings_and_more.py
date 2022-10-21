# Generated by Django 4.1 on 2022-10-19 01:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("checkout", "0001_initial"), ("accounts", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="address",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="accounts.address",
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="bookings",
            field=models.ManyToManyField(to="checkout.booking"),
        ),
        migrations.AddField(
            model_name="customuser",
            name="paymentcard1",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="card_1",
                to="accounts.paymentcard",
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="paymentcard2",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="card_2",
                to="accounts.paymentcard",
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="paymentcard3",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name="card_3",
                to="accounts.paymentcard",
            ),
        ),
        migrations.AddField(
            model_name="customuser",
            name="status",
            field=models.ForeignKey(
                default=2,
                on_delete=django.db.models.deletion.PROTECT,
                to="accounts.customersatus",
            ),
        ),
    ]
