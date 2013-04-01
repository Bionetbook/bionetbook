from django.contrib import admin
from workflow.models import Workflow, WorkflowProtocol

admin.site.register(Workflow)
admin.site.register(WorkflowProtocol)
