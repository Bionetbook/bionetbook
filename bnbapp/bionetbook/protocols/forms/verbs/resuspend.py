from protocols.forms import forms


class ResuspendForm(forms.VerbForm):

    name = "Resuspend"
    slug = "resuspend"
    has_component = True

    item_to_act = forms.CharField(required=False, help_text='what are you resuspending?', label='item to resuspend')
    edit_remarks = forms.CharField(required=False)
