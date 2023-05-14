from django import forms
from django.forms import ModelForm
from .models import Ticket, Comment


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title','description', 'priority']

class CommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control', 'rows' : '3'}))
        