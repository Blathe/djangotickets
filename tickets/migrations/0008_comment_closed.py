# Generated by Django 4.1.1 on 2022-09-24 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0007_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='closed',
            field=models.IntegerField(default=0),
        ),
    ]
