# Generated by Django 4.0.6 on 2022-08-09 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='active_status',
            field=models.BooleanField(default=True),
        ),
    ]
