# Generated by Django 3.1.7 on 2021-04-11 21:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('httpsrv', '0022_remove_question_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='CourseSubscriptions',
            new_name='CourseSubscription',
        ),
    ]
