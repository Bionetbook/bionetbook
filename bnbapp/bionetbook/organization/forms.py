from django import forms
from organization.models import Membership, Organization

class MembershipForm(forms.ModelForm):

    class Meta:
        model = Membership


class OrganizationForm(forms.ModelForm):

    class Meta:
        model = Organization




