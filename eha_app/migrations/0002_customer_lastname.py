# Generated by Django 3.1.7 on 2021-05-20 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eha_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='lastname',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
