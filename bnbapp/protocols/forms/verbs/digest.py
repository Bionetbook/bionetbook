from protocols.forms import forms


class DigestForm(forms.VerbForm):

    name = "Digest"
    slug = "digest"
    has_machine = True

    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')
    digest_input = forms.CharField(required = False, help_text = 'name of target DNA strand')
    digest_output = forms.CharField(required = False, help_text = 'fragment after digestion')
    enzyme = forms.CharField(required = False)
    Buffer = forms.CharField(required = False)

