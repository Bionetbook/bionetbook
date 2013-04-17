from django.contrib import admin

from protocols.models import Protocol

class ProtocolAdmin(admin.ModelAdmin):
	list_display = ('name','public','published')

admin.site.register(Protocol, ProtocolAdmin)