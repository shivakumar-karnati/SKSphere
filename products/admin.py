from django.contrib import admin
from .models import Category, Product, Wishlist, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name"
    )

    search_fields = (
        "name",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "category",
        "price",
        "stock",
        "featured",
        "trending",
        "best_seller",
        "created_at"
    )
    list_editable = (
        "stock",
        "featured",
        "trending",
        "best_seller"
    )

    list_filter = (
        "category",
        "featured",
        "trending",
        "best_seller",
        "created_at"
    )

    search_fields = (
        "name",
        "description"
    )

    ordering = (
        "-created_at",
    )


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "product",
        "created_at"
    )

    search_fields = (
        "user__username",
        "product__name"
    )

    list_filter = (
        "created_at",
    )


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "product",
        "rating",
        "created_at"
    )

    search_fields = (
        "user__username",
        "product__name"
    )

    list_filter = (
        "rating",
        "created_at"
    )

    ordering = (
        "-created_at",
    )