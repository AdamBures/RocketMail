# Generated by Django 4.0.6 on 2023-05-01 18:19

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_rename_gmail_passwords_user_gmail_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default=main.models.get_default, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gmail_password',
            field=models.CharField(default=main.models.get_default, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gmail_username',
            field=models.CharField(default=main.models.get_default, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(default=main.models.get_default, max_length=100, null=True),
        ),
    ]
