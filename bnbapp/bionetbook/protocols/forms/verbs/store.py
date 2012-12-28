from protocols import forms


class StoreForm(forms.VerbForm):

    name = "Store"
    slug = "store"

    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
    duration_min_time = forms.IntegerField()
    edit_what_remark = forms.CharField()
    edit_remarks = forms.CharField()
    edit_vessel_type = forms.CharField()
