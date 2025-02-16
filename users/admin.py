from django.contrib import admin
from .models import User, CustomSession


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "username", "phone_number", "date_joined")
    search_fields = ("name", "username", "phone_number")
    list_filter = ("date_joined",)
    ordering = ("date_joined",)
    readonly_fields = ("id", "date_joined")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "name",
                    "username",
                    "phone_number",
                    "gender",
                    "age",
                    "height",
                    "date_joined"
                )
            }
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": ("id", "name", "username", "phone_number"),
            },
        ),
    )


@admin.register(CustomSession)
class CustomSessionAdmin(admin.ModelAdmin):
    list_display = ("user", "ip_address", "device_info", "last_online", "created_at")
    search_fields = ("user__username", "user__id", "ip_address", "device_info")
    list_filter = ("last_online", "created_at")
    ordering = ("last_online",)
    readonly_fields = ("sessionid", "last_online", "created_at")
    fieldsets = (
        (
            None,
            {"fields": ("user", "sessionid", "ip_address", "device_info", "last_online", "created_at")},
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": ("user", "sessionid", "ip_address", "device_info"),
            },
        ),
    )
