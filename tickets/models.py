from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Ticket(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed')
    )
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    )

    title = models.CharField(max_length=80)
    description = models.TextField(max_length=200)
    creation_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="OPEN")
    priority = models.CharField(choices=PRIORITY_CHOICES, max_length=20, default="MEDIUM")

    def __str__(self):
        return self.title;

class Comment(models.Model):
    TAG_CHOICES = (
        ('DEFAULT', 'Default'),
        ('CLOSED', 'Closed'),
        ('REOPENED', 'Reopened'),
    )
    creation_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    body = models.CharField(max_length=200)
    tag = models.CharField(choices=TAG_CHOICES, max_length=20, default="DEFAULT")