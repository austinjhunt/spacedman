# Generated by Django 3.1.7 on 2021-04-07 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('httpsrv', '0014_auto_20210407_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question_user',
            name='increment',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='question_user',
            name='remaining',
            field=models.IntegerField(default=1),
        ),
    ]
