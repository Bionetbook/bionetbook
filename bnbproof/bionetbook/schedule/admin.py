from django.contrib import admin

from schedule.models import Schedule, Event

admin.site.register(Schedule)
admin.site.register(Event)
