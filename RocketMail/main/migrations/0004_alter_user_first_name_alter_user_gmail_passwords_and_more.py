# Generated by Django 4.0.6 on 2023-05-01 17:55

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_user_first_name_user_gmail_passwords_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default=main.models.get_default, max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='gmail_passwords',
            field=models.CharField(default=main.models.get_default, max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='gmail_username',
            field=models.CharField(default=main.models.get_default, max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default=main.models.get_default, max_length=100),
        ),
    ]
