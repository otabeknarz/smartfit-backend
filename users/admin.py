from django.contrib import admin
from .models import User, CustomSession, Payment


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "username", "phone_number", "date_joined")
    search_fields = ("name", "username", "phone_number")
    list_filter = ("date_joined",)
    ordering = ("date_joined",)
    readonly_fields = ("id", "date_joined")
    fieldsets = (
        (
            "Main information",
            {
                "fields": (
                    "id",
                    "name",
                    "picture",
                    "username",
                    "phone_number",
                    "gender",
                    "age",
                    "height",
                    "date_joined",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": ("id", "name", "picture", "username", "phone_number"),
            },
        ),
    )


@admin.register(CustomSession)
class CustomSessionAdmin(admin.ModelAdmin):
    list_display = ("user", "ip_address", "device_info", "last_online", "created_at")
    search_fields = ("user__username", "user__id", "ip_address", "device_info")
    list_filter = ("last_online", "created_at")
    ordering = ("last_online",)
    readonly_fields = ("token", "last_online", "created_at")
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "token",
                    "ip_address",
                    "device_info",
                    "last_online",
                    "created_at",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": ("user", "token", "ip_address", "device_info"),
            },
        ),
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "currency", "method", "status")
    search_fields = (
        "user__username",
        "user__id",
        "user__name",
    )
    list_filter = ("status",)
    ordering = ("status",)
