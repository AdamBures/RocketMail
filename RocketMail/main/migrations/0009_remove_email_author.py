# Generated by Django 4.0.6 on 2023-05-02 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_remove_email_ipfs_remove_email_content_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='email',
            name='author',
        ),
    ]
