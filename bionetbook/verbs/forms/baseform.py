import floppyforms as forms


class BaseForm(forms.Form):

    name = NotImplemented()
    slug = NotImplemented()

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
