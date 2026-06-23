from django.contrib import admin
from .models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'product',
        'quantity',
        'added_at',
    )
    list_editable = ('quantity',)

    list_filter = (
        'added_at',
        'user',
    )

    search_fields = (
        'user__username',
        'product__name',
    )

    ordering = (
        '-added_at',
    )

    autocomplete_fields = (
        'user',
        'product',
    )