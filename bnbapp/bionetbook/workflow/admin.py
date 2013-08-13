from django.contrib import admin
from workflow.models import Workflow


class WorkflowAdmin(admin.ModelAdmin):
	list_display = ('slug','user')

admin.site.register(Workflow,WorkflowAdmin)

admin.site.register(Workflow)
