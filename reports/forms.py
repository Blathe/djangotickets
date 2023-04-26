from django import forms

from django.contrib.auth.models import User
from django.forms import ModelChoiceField

class UserChoiceField(ModelChoiceField):

    def label_from_instance(self, obj):
        return f'{obj.first_name} {obj.last_name}'
    
class ReportGenerationForm(forms.Form):
    STATUS_CHOICES = (
        ('ANY', 'Any'),
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed')
    )
    
    TIME_CHOICES = (
        ('LAST 7 DAYS', 'Last 7 Days'),
        ('LAST 30 DAYS', 'Last 30 Days'),
        ('ALL TIME', 'All Time')
    )
    
    GROUP_BY_CHOICES = (
        ('USER', 'User'),
        ('STATUS', 'Status'),
        ('PRIORITY', 'Priority')
    )
      
    user = UserChoiceField(queryset=User.objects.all(), empty_label="All", required=False)
    status = forms.ChoiceField(choices = STATUS_CHOICES, required=False)
    time = forms.ChoiceField(choices = TIME_CHOICES, initial='ALL TIME')
    group_by = forms.ChoiceField(choices = GROUP_BY_CHOICES, initial='PRIORITY')
    
    
    