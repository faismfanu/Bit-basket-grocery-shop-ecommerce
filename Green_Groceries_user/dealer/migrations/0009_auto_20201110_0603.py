# Generated by Django 3.1.2 on 2020-11-10 06:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dealer', '0008_auto_20201109_0858'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shippingadress',
            old_name='zipcode',
            new_name='pincode',
        ),
    ]
