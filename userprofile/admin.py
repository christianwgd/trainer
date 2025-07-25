from django.contrib import admin

from userprofile.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['ref_usr']
    autocomplete_fields = ['exclude']
