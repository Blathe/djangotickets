from django.forms import ModelForm
from .models import Ticket, Comment

class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title','description', 'priority']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']