from django import forms
from feedback.models import Feedback

class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ['name', 'email', 'classification', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class':'textarea span5'}),
        }



    # class Meta:
    #     model = Event
    #     fields = ['description']
    #     widgets = {
    #         'description': forms.Textarea(attrs={'rows': 3, 'class':'textarea span12'}),
    #     }
