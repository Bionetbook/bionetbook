import floppyforms as forms

from steps.models import Step


class StepForm(forms.ModelForm):

    class Meta:
        model = Step
        exclude = ('protocol', 'slug', 'duration_in_seconds', )
