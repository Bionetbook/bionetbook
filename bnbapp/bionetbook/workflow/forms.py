from django import forms
from workflow.models import Workflow


class WorkflowForm(forms.ModelForm):

    class Meta:
        model = Workflow
        #exclude = ('parent', 'slug', 'duration_in_seconds', 'status','raw')
        exclude = ('slug', 'duration', 'author', 'owner', 'protocols')
