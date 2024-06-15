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
