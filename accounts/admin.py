from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'phone',
        'city',
    )

    search_fields = (
        'user__username',
        'phone',
        'city',
    )

    list_filter = (
        'city',
    )

    ordering = (
        'user__username',
    )

    list_select_related = (
        'user',
    )

    readonly_fields = (
        'user',
    )