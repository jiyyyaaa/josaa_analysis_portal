# forms.py

from django import forms
from .models import rank_data

class RankForm(forms.Form):
    GENDER_CHOICES = [
        ('Female-only (including Supernumerary)', 'Female-only (including Supernumerary)'),
        ('Gender-Neutral', 'Gender-Neutral'),
    ]

    SEAT_TYPE_CHOICES = [
        ('OPEN', 'OPEN'),
        ('EWS', 'EWS'),
        ('OBC-NCL', 'OBC-NCL'),
        ('OPEN (PwD)', 'OPEN (PwD)'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('EWS (PwD)', 'EWS (PwD)'),
        ('SC (PwD)', 'SC (PwD)'),
        ('ST (PwD)', 'ST (PwD)'),
        ('OBC-NCL (PwD)', 'OBC-NCL (PwD)'),
    ]

    rank = forms.IntegerField(label='Rank', required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    seat_type = forms.ChoiceField(choices=SEAT_TYPE_CHOICES, required=True)

class CollegeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['college'] = forms.ModelChoiceField(queryset=rank_data.objects.values_list('institute', flat=True).distinct(), empty_label='Select an IIT')

class RankDifferenceForm(forms.Form):
    SEAT_TYPE_CHOICES = [
        ('OPEN', 'OPEN'),
        ('EWS', 'EWS'),
        ('OBC-NCL', 'OBC-NCL'),
        ('OPEN (PwD)', 'OPEN (PwD)'),
        ('SC', 'SC'),
        ('ST', 'ST'),
        ('EWS (PwD)', 'EWS (PwD)'),
        ('SC (PwD)', 'SC (PwD)'),
        ('ST (PwD)', 'ST (PwD)'),
        ('OBC-NCL (PwD)', 'OBC-NCL (PwD)'),
    ]

    institute = forms.ModelChoiceField(queryset=rank_data.objects.values_list('institute', flat=True).distinct(), empty_label='Select an Institute')
    program = forms.ModelChoiceField(queryset=rank_data.objects.values_list('program', flat=True).distinct(), empty_label='Select a Branch/Program')
    seat_type = forms.ChoiceField(choices=SEAT_TYPE_CHOICES, required=True)