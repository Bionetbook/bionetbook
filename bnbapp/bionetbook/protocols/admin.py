from django.contrib import admin

from protocols.models import Protocol, Reference

class ProtocolAdmin(admin.ModelAdmin):
	list_display = ('slug','public','published','author','owner')

    def save_model(self, request, obj, form, change):
        # obj.user = request.user
        obj.rebuild_steps()		# THIS GETS TWEAKED BY THE ADMIN FORM
        obj.save()


admin.site.register(Protocol, ProtocolAdmin)
admin.site.register(Reference)