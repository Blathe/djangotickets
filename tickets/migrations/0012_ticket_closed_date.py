# Generated by Django 4.1.2 on 2023-04-20 19:13

from django.db import migrations, models
from django.utils.timezone import now

def add_default_closed_dates(apps, schema_editor):

    Ticket = apps.get_model("tickets", "Ticket")
    for ticket in Ticket.objects.all():
        if ticket.status == "CLOSED":
            ticket.closed_date = now()
            ticket.save()

class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0011_alter_comment_body_alter_ticket_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='closed_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.RunPython(add_default_closed_dates),
        
    ]
