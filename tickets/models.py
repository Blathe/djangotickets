from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Ticket(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed')
    )
    PRIORITY_CHOICES = (
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=600)
    creation_date = models.DateTimeField(auto_now_add=True)
    closed_date = models.DateTimeField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default="OPEN")
    priority = models.PositiveIntegerField(choices=PRIORITY_CHOICES, default=2)

    ''' Adjusting the __str__ will give our model a name in the Django admin '''
    def __str__(self):
        return f"{self.title} - Priority: {self.priority}"
    
    def get_comments(self):
        comments = Comment.objects.all()
        return comments.filter(ticket=self.id)

    def change_priority(self, priority):
        self.priority = priority
        self.save
    
class Comment(models.Model):
    TAG_CHOICES = (
        ('DEFAULT', 'Default'),
        ('CLOSED', 'Closed'),
        ('REOPENED', 'Reopened'),
    )
    creation_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    body = models.CharField(max_length=400)
    tag = models.CharField(choices=TAG_CHOICES, max_length=20, default="DEFAULT")
    
    ''' Adjusting the __str__ will give our model a name in the Django admin'''
    def __str__(self):
        return f"{self.id} - Owner: {self.owner} | Ticket: {self.ticket.id} -- {self.body}"