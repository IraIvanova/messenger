# Generated by Django 5.0.3 on 2024-03-05 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('custom_user', '0002_alter_customuser_managers_alter_customuser_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='profile',
        ),
    ]
