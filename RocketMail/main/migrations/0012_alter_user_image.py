# Generated by Django 4.0.6 on 2023-05-06 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_user_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default='static/images/default.jpg', upload_to='static/images/'),
        ),
    ]
