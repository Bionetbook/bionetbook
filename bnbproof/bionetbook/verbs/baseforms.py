import floppyforms as forms


class VerbForm(forms.Form):

    name = NotImplemented
    slug = NotImplemented

    @classmethod
    def display_fields(cls):
        fields = []
        for k, v in cls.base_fields.items():
            d = dict(
                field_name=k.replace("_", " "),
                field_slug=k,
                data=v
            )
            fields.append(d)
        return fields

forms.VerbForm = VerbForm
