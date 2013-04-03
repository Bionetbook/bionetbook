from protocols.forms import forms


class DecantForm(forms.VerbForm):

    name = "Decant"
    slug = "decant"
    has_machine = True

    edit_what_remark = forms.CharField()
    duration = forms.IntegerField(help_text='this is the minimal time this should take', initial = 'sec')