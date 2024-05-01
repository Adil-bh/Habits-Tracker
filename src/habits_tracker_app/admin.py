from django.contrib import admin

from habits_tracker_app.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name")
    list_editable = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
