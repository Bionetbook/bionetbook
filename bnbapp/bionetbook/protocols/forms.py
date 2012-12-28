#import floppyforms as forms
from django import forms

from protocols.models import Protocol


class ProtocolForm(forms.ModelForm):

    class Meta:
        model = Protocol
        exclude = ('parent', 'owner', 'slug', 'duration_in_seconds', 'status', 'version',)


class PublishForm(forms.Form):
    pass


class StepForm(forms.Form):
    name = forms.CharField(max_length=100)
    remark = forms.CharField()


class ActionForm(forms.Form):

    #VERB_CHOICES = (('add','Add'), ('mix','Mix'))

    name = forms.CharField(max_length=100)
    remark = forms.CharField()
    duration = forms.IntegerField()
    #verb = forms.ChoiceField(choices=VERB_CHOICES)


class VerbForm(forms.Form):
    pass

###########
# VERB FORMS

class VerbAddForm(VerbForm):

    name = "Add"  # cannot silence the name without an error, the name here is redundant
    slug = "add"

    duration_min_time = forms.IntegerField()
    describe_where = forms.CharField()
    edit_remarks = forms.CharField()
    add_what = forms.CharField()


class VerbApplyForm(VerbForm):

    name = "Apply"
    slug = "apply"

    edit_what_remark = forms.CharField()
    describe_where = forms.CharField()
    duration_min_time = forms.IntegerField()
    edit_remarks = forms.CharField()
    specify_tool = forms.CharField()
    comment_why = forms.CharField()
