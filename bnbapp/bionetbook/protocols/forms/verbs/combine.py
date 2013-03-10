from protocols.forms import forms


class CombineForm(forms.VerbForm):

    name = "Combine"
    slug = "combine"
    has_component = True


    min_temp = forms.IntegerField()
    max_temp = forms.IntegerField()
    duration_min_time = forms.IntegerField() # remove this
    describe_where = forms.CharField()
    edit_remarks = forms.CharField()

    # add these:
    # description = forms.CharField()
    # add_reagents = forms.CharField(required = False, helptext='500 ng oligoDt | CaCl2, 5M 20 ml' )
    # bring_volume_to = forms.CharField(required=False, helptext='12 ul, ddw')