from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'user_email',
        'phone',
        'city',
    )

    search_fields = (
        'user__username',
        'user__email',
        'user__first_name',
        'user__last_name',
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

    @admin.display(description='Email')
    def user_email(self, obj):
        return obj.user.email