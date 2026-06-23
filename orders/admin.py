from django.contrib import admin
from django.utils.html import format_html
from .models import Order, OrderItem,Payment,Coupon

class OrderItemInline(admin.TabularInline):

    model = OrderItem
    extra = 0
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'colored_status',
        'id',
        'user',
        'get_product_name',
        'payment_method',
        'total_amount',
        'status',
        'created_at'

    )
    
    list_editable = (
        'status',
    )

    def get_product_name(self, obj):

        products = obj.orderitem_set.all()

        return ", ".join(
            [item.product.name for item in products]
        )

    get_product_name.short_description = "Products"


    list_filter = (
        'payment_method',
        'status',
        'created_at'

    )

    search_fields = (

        'user__username',
        

    )
    def colored_status(self, obj):

        if obj.status == "payment Verification":
            color = "orange"

        elif obj.status == "Processing":
            color = "blue"
        elif obj.status == "Shipped":
            color = "yellow"
        elif obj.status == "Delivered":
            color = "green"

        else:
            color = "red"

        return format_html(
            '<strong style="color:{};">{}</strong>',
            color,
            obj.status
        )

    colored_status.short_description = "Status"

    inlines = [OrderItemInline] 

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):

    list_display = (

        'id',
        'order',
        'product',
        'quantity',
        'price'

    )

    search_fields = (

        'product__name',

    )
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'get_user',
        'order',
        'get_product_name',
        'get_total_amount',
        'get_payment_method',
        'payment_status',
        'uploaded_at'
    )
    list_editable = (
        'payment_status',
    )

    def get_product_name(self, obj):

        products = obj.order.orderitem_set.all()

        return ", ".join(
            [item.product.name for item in products]
        )

    get_product_name.short_description = "Products"


    search_fields = (
        'order__user__username',
        'order__full_name'
    )

    list_filter = (
        'order__payment_method',
        'uploaded_at'
    )

    def get_user(self, obj):
        return obj.order.user.username

    get_user.short_description = "User"

    def get_full_name(self, obj):
        return obj.order.full_name

    get_full_name.short_description = "Customer"

    def get_total_amount(self, obj):
        return obj.order.total_amount
    
    get_total_amount.short_description = "Amount"

    def get_payment_method(self, obj):
        return obj.order.get_payment_method_display()

    get_payment_method.short_description = "Payment"
    


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):

    list_display = (
        'code',
        'discount',
        'minimum_amount',
        'active',
        'expiry_date'
    )

    list_filter = (
        'active',
    )