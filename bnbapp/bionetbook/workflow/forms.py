from django import forms
from workflow.models import Workflow


class WorkflowForm(forms.ModelForm):

    class Meta:
        model = Workflow

