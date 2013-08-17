from django.contrib import admin
from experiment.models import Experiment

class ExperimentAdmin(admin.ModelAdmin):
	list_display = ('user','name','workflow')
admin.site.register(Experiment,ExperimentAdmin)