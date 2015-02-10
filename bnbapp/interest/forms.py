from django import forms
from interest.models import Interest

class InterestForm(forms.ModelForm):

    class Meta:
        model = Interest




