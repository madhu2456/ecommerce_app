# Generated by Django 2.0.4 on 2018-04-30 06:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('addresses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='billing_profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='billing.BillingProfile'),
        ),
    ]
