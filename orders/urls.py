from django.urls import path
from .views import checkout,place_order,payment_pending,my_orders,order_detail,payment_page,save_checkout,cancel_order,download_invoice,apply_coupon,buy_now,buy_now_checkout,buy_now_decrease,buy_now_increase,apply_buy_now_coupon,remove_buy_now_coupon,place_buy_now_order,order_success,save_buy_now_checkout

urlpatterns = [

    path('checkout/',checkout,name='checkout'),

    path('place-order/',place_order,name='place_order'),

    path('payment-pending/',payment_pending,name='payment_pending'),

    path('my-orders/',my_orders,name='my_orders'),

    path('order/<int:id>/',order_detail,name='order_detail'),

    path('payment/',payment_page,name='payment'),

    path('save-checkout/',save_checkout,name='save_checkout'),

    path('cancel-order/<int:order_id>/',cancel_order,name='cancel_order'),

    path('invoice/<int:order_id>/',download_invoice,name='download_invoice'),

    path(
            'apply-coupon/',
            apply_coupon,
            name='apply_coupon'
        ),
    path(
        'buy-now/<int:product_id>/',
        buy_now,
        name='buy_now'
    ),
    path(
        'buy-now-checkout/',
        buy_now_checkout,
        name='buy_now_checkout'
    ),

    path(
        'buy-now/increase/',
        buy_now_increase,
        name='buy_now_increase'
    ),

    path(
        'buy-now/decrease/',
        buy_now_decrease,
        name='buy_now_decrease'
    ),
    path(
        'buy-now/apply-coupon/',
        apply_buy_now_coupon,
        name='apply_buy_now_coupon'
    ),

    path(
        'buy-now/remove-coupon/',
        remove_buy_now_coupon,
        name='remove_buy_now_coupon'
    ),
    path(
        'save-buy-now-checkout/',
        save_buy_now_checkout,
        name='save_buy_now_checkout'
    ),
    path(
    'place-buy-now-order/',
    place_buy_now_order,
    name='place_buy_now_order'
    ),
    path(
        'order_success/',
        order_success,
        name='order_success'
    ),

]