from django.contrib import admin

from protocols.models import Protocol, Reference

class ProtocolAdmin(admin.ModelAdmin):
    list_display = ('slug','public','published','author','owner')

    def save_model(self, request, obj, form, change):
        obj.rebuild_steps()     # THIS GETS TWEAKED BY THE ADMIN FORM
        obj.save(editor=request.user)


admin.site.register(Protocol, ProtocolAdmin)
admin.site.register(Reference)