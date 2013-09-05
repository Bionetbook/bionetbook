from django import forms
from workflow.models import Workflow
from django.db.models.query import EmptyQuerySet
from django.utils.translation import ugettext_lazy as _

class WorkflowForm(forms.ModelForm):

    class Meta:
        model = Workflow
        #exclude = ('parent', 'slug', 'duration_in_seconds', 'status','raw')
        exclude = ('slug', 'duration', 'author', 'owner', 'protocols')


class WorkflowManualForm(forms.Form):
    # name = forms.CharField( widget=forms.TextInput(attrs={'class':'special'}) )
    name = forms.CharField( widget=forms.TextInput() )
    protocols = forms.ModelChoiceField(required=False, queryset=EmptyQuerySet(), label=_("Protocol"), widget=forms.CheckboxSelectMultiple())

    # UPDATE IT IN THE VIEW
    # form.fields['protocols'] = forms.ModelChoiceField( queryset=self.request.user.profile.get_published_protocols_qs(), label=_("Protocol"), widget=forms.CheckboxSelectMultiple() )
