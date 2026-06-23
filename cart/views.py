from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
from .models import Cart
from products.models import Product
from django.contrib import messages
from orders.models import Coupon



@login_required
def add_to_cart(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if product.stock <= 0:

        messages.error(
            request,
            f"{product.name} is out of stock."
        )

        return redirect(
            'product_detail',
            id = product_id
        )

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product
    )

    if not created:

        if cart_item.quantity < product.stock:

            cart_item.quantity += 1
            cart_item.save()

            messages.success(
                request,
                f"{product.name} quantity updated."
            )

        else:

            messages.warning(
                request,
                f"Only {product.stock} items available."
            )

    else:

        messages.success(
            request,
            f"{product.name} added to cart."
        )

    return redirect('cart')

@login_required
def cart_page(request):

    cart_items = Cart.objects.filter(
        user=request.user
    ).select_related(
        'product'
    )

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    discount = 0

    coupon_id = request.session.get(
        'coupon_id'
    )

    coupon = None

    if coupon_id:

        try:

            coupon = Coupon.objects.get(
                id=coupon_id
            )

            if (
                coupon.is_valid()
                and
                total >= coupon.minimum_amount
            ):

                discount = (
                    total *
                    coupon.discount
                ) / 100

        except Coupon.DoesNotExist:

            request.session.pop(
                'coupon_id',
                None
            )

    final_total = total - discount

    request.session[
        'final_total'
    ] = float(final_total)

    return render(
        request,
        'cart/cart.html',
        {
            'cart_items': cart_items,
            'total': total,
            'discount': discount,
            'final_total': final_total,
            'coupon': coupon
        }
    )

@login_required
def increase_quantity(request, cart_id):

    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)

    cart_item.quantity += 1

    cart_item.save()

    return redirect('cart')


@login_required
def decrease_quantity(request, cart_id):

    cart_item = get_object_or_404(Cart,id=cart_id)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


@login_required
def remove_from_cart(request, cart_id):

    cart_item = get_object_or_404(Cart,id=cart_id)

    cart_item.delete()

    return redirect('cart')

