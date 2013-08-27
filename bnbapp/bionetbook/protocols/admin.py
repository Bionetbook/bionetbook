from django.contrib import admin

from protocols.models import Protocol, Reference

class ProtocolAdmin(admin.ModelAdmin):
	list_display = ('slug','public','published','author','owner')


admin.site.register(Protocol, ProtocolAdmin)
admin.site.register(Reference)