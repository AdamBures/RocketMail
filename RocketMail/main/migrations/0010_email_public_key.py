# Generated by Django 4.0.6 on 2023-05-02 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_remove_email_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='public_key',
            field=models.CharField(default='', max_length=100),
        ),
    ]