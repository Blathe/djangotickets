from django import forms

from django.contrib.auth.models import User
from django.forms import ModelChoiceField

class UserChoiceField(ModelChoiceField):

    # this function is needed to format the first + last name in a User Choice Field
    def label_from_instance(self, obj):
        return f'{obj.first_name} {obj.last_name}'
    
class ReportGenerationForm(forms.Form):
    STATUS_CHOICES = (
        ('ANY', 'Any'),
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed')
    )
    
    TIME_CHOICES = (
        ('ALL TIME', 'All Time'),
        ('LAST 7 DAYS', 'Last 7 Days'),
        ('LAST 30 DAYS', 'Last 30 Days'),
    )
    
    GROUP_BY_CHOICES = (
        ('USER', 'User'),
        ('STATUS', 'Status'),
        ('PRIORITY', 'Priority')
    )
      
    #Define our form fields
    #name is an optional field
    name = forms.CharField(max_length=120, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    user = UserChoiceField(queryset=User.objects.all(), empty_label="Any", required=False, label="Ticket Owner",
    widget=forms.Select(attrs={'class': 'form-select'}))
    status = forms.ChoiceField(choices = STATUS_CHOICES, required=False, label="Ticket Status",
    widget=forms.Select(attrs={'class': 'form-select'}))
    time = forms.ChoiceField(choices = TIME_CHOICES, initial='ALL TIME', label="Date Created",
    widget=forms.Select(attrs={'class': 'form-select'}))
    group_by = forms.ChoiceField(choices = GROUP_BY_CHOICES, initial='PRIORITY', label="Group By",
    widget=forms.Select(attrs={'class': 'form-select'}))
    
    
    