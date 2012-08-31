from verbs.baseforms import forms


class CookForm(forms.VerbForm):

    name = "cook"
    slug = "cook"

    duration_in_seconds = forms.IntegerField()

    @classmethod
    def display_fields(cls):
        fields = []
        for k, v in cls.base_fields.items():
            d = dict(
                field_name=k.replace("_", " ").capitalize(),
                data=v
            )
            fields.append(d)
        return fields
