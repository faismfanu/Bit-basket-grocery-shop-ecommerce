# Generated by Django 2.0.2 on 2020-11-20 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dealer', '0024_auto_20201119_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='offer_percentage',
            field=models.IntegerField(null=True),
        ),
    ]
