# Generated by Django 3.1.7 on 2021-04-11 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('httpsrv', '0023_auto_20210411_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='account_type',
            field=models.CharField(choices=[('instructor', 'Instructor'), ('student', 'Student')], default='student', max_length=30),
        ),
        migrations.AlterField(
            model_name='coursesubscription',
            name='subscription_timestamp',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
