# Generated by Django 4.1.1 on 2022-10-02 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0010_alter_ticket_priority'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.CharField(max_length=400),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.TextField(max_length=600),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='title',
            field=models.CharField(max_length=200),
        ),
    ]
