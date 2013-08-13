from django.contrib import admin
from experiment.models import Experiment

class ExperimentAdmin(admin.ModelAdmin):
	list_display = ('user','calendar','name')
admin.site.register(Experiment,ExperimentAdmin)