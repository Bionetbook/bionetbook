from django import forms
from history.models import History

class HistoryForm(forms.ModelForm):

    class Meta:
        model = History




