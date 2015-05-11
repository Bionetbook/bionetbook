from django.contrib import admin

from profiles.models import Profile, Favorite

admin.site.register(Profile)
admin.site.register(Favorite)
