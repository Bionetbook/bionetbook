from django.contrib import admin

from schedule.models import Calendar

class CalendarAdmin(admin.ModelAdmin):
	list_display = ('name','user')

admin.site.register(Calendar,CalendarAdmin)

