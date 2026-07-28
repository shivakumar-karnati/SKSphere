from django.shortcuts import render,redirect
from cart.models import Cart
from .models import Order,OrderItem,Payment
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Coupon
from django.shortcuts import get_object_or_404
from decimal import Decimal
from django.http import HttpResponse

from reportlab.pdfgen import canvas

from reportlab.lib.pagesizes import letter
from products.models import Product
import os
from django.conf import settings

from django.core.mail import send_mail
import qrcode
import base64
from django.db.models import Case, When, IntegerField
from io import BytesIO

@login_required
def checkout(request):

    request.session['checkout_type'] = 'cart'
    cart_items = Cart.objects.filter(
        user=request.user
    )

    if not cart_items.exists():

        messages.error(
            request,
            "Your cart is empty."
        )

        return redirect('cart')

    total = sum(
        item.product.price * item.quantity
        for item in cart_items
    )

    discount = 0
    coupon = None

    coupon_id = request.session.get(
        'checkout_coupon_id'
    )

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
                    total * coupon.discount
                ) / 100

        except Coupon.DoesNotExist:

            request.session.pop(
                'checkout_coupon_id',
                None
            )

    final_total = total - discount

    request.session[
        'final_total'
    ] = str(final_total)
    request.session.pop(
        'buy_now_product',
        None
    )

    request.session.pop(
        'buy_now_qty',
        None
    )

    request.session.pop(
        'buy_now_total',
        None
    )

    request.session.pop(
        'buy_now_coupon_id',
        None
    )
    return render(
        request,
        'orders/checkout.html',
        {
            'cart_items': cart_items,
            'total': total,
            'discount': discount,
            'final_total': final_total,
            'coupon': coupon
        }
    )


@login_required
def save_checkout(request):

    if request.method == "POST":

        request.session['full_name'] = request.POST.get('full_name')

        request.session['address'] = request.POST.get('address')

        request.session['phone'] = request.POST.get('phone')

        request.session['city'] = request.POST.get('city')
        request.session['payment_method'] = request.POST.get(
                'payment_method'
            )
        payment_method = request.session[
            'payment_method'
        ]
        if payment_method == "COD":

            return redirect(
                'place_order'
            )

        return redirect(
            'payment'
        )

    return redirect(
        'checkout'
    )


@login_required
def place_order(request):


    cart_items = Cart.objects.filter(
        user=request.user
    )

    if not cart_items.exists():

        messages.error(
            request,
            "Cart is empty."
        )

        return redirect('cart')

    final_total = Decimal(
            request.session.get(
                'final_total'
            )
        
            )

    if final_total is None:

        messages.error(
            request,
            "Checkout expired."
        )

        return redirect('checkout')

    for item in cart_items:

        if item.quantity > item.product.stock:

            messages.error(
                request,
                f"Only {item.product.stock} units of {item.product.name} available."
            )

            return redirect('cart')
    payment_method = request.session[
            'payment_method'
        ]
    order = Order.objects.create(

        user=request.user,

        full_name=request.session.get(
            'full_name'
        ),

        phone=request.session.get(
            'phone'
        ),

        address=request.session.get(
            'address'
        ),

        city=request.session.get(
            'city'
        ),
        payment_method=payment_method,
        total_amount=final_total,

        status='payment Verification'
    )

    for item in cart_items:

        OrderItem.objects.create(

            order=order,

            product=item.product,

            quantity=item.quantity,

            price=item.product.price
        )

        item.product.stock -= item.quantity
        item.product.save()

    screenshot = request.FILES.get(
        'screenshot'
    )

    if screenshot:

        Payment.objects.create(
            order=order,
            screenshot=screenshot
        )

    send_order_email(order)

    cart_items.delete()

    request.session.pop(
    'checkout_type',
    None
)

    request.session.pop(
        'buy_now_product',
        None
    )

    request.session.pop(
        'buy_now_qty',
        None
    )

    request.session.pop(
        'buy_now_total',
        None
    )

    request.session.pop(
        'buy_now_coupon_id',
        None
    )

    request.session.pop(
        'checkout_coupon_id',
        None
    )

    request.session.pop(
        'final_total',
        None
    )

    request.session.pop(
        'final_total',
        None
    )

    request.session.pop(
        'full_name',
        None
    )

    request.session.pop(
        'address',
        None
    )

    request.session.pop(
        'phone',
        None
    )

    request.session.pop(
        'city',
        None
    )

    messages.success(
        request,
        "Order placed successfully."
    )

    if payment_method == "COD":

        return redirect(
            'order_success'
        )

    return redirect(
        'payment_pending'
    )



@login_required
def download_invoice(request, order_id):

    order = Order.objects.get(
        id=order_id,
        user=request.user
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response[
        'Content-Disposition'
    ] = f'attachment; filename="invoice_{order.id}.pdf"'

    p = canvas.Canvas(
        response,
        pagesize=letter
    )

    # Header

    p.setFont(
    "Helvetica-Bold",
    24
    )
    
    logo_path = os.path.join(
        settings.BASE_DIR,
        'static',
        'images',
        'SKSphere logo.png'
    )

    if os.path.exists(
        logo_path
    ):
        p.drawImage(
            logo_path,
            430,
            720,
            width=120,
            height=60
        )

    p.drawString(
        50,
        760,
        "SKSphere"
    )

    p.setFont(
        "Helvetica",
        12
    )

    p.drawString(
        50,
        740,
        "Premium E-Commerce Platform"
    )

    # Order Info

    p.setFont(
        "Helvetica",
        12
    )

    p.drawString(
        50,
        710,
        f"Order ID: {order.id}"
    )

    p.drawString(
        50,
        690,
        f"Customer: {order.full_name}"
    )

    p.drawString(
        50,
        670,
        f"Phone: {order.phone}"
    )

    p.drawString(
        50,
        650,
        f"City: {order.city}"
    )

    p.drawString(
        50,
        630,
        f"Status: {order.status}"
    )

    p.drawString(
        50,
        610,
        f"Date: {order.created_at.strftime('%d-%m-%Y')}"
    )

    # Products

    y = 560

    p.setFont(
        "Helvetica-Bold",
        14
    )

    p.drawString(
        50,
        y,
        "Products"
    )

    y -= 30

    total = 0

    for item in order.orderitem_set.all():

        subtotal = (
            item.price *
            item.quantity
        )

        total += subtotal

        p.setFont(
            "Helvetica",
            12
        )

        p.drawString(
            50,
            y,
            f"{item.product.name}"
        )

        p.drawString(
            250,
            y,
            f"Qty: {item.quantity}"
        )

        p.drawString(
            350,
            y,
            f"₹{subtotal}"
        )

        y -= 25

    # Total

    y -= 20

    p.setFont(
        "Helvetica-Bold",
        14
    )

    p.drawString(
        50,
        y,
        f"Total Amount: ₹{order.total_amount}"
    )

    p.save()

    return response


def payment_pending(request):

    return render(
        request,
        'orders/payment_pending.html'
    )


@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).annotate(

        status_order=Case(

            When(
                status='Payment Verification',
                then=0
            ),

            When(
                status='Processing',
                then=1
            ),

            When(
                status='Shipped',
                then=2
            ),

            When(
                status='Delivered',
                then=3
            ),

            When(
                status='Cancelled',
                then=4
            ),

            output_field=IntegerField()
        )

    ).order_by(
        'status_order',
        '-created_at'
    )

    return render(
        request,
        'orders/my_orders.html',
        {
            'orders': orders
        }
    )


@login_required
def order_detail(request, id):

    order = get_object_or_404(
        Order,
        id=id,
        user=request.user
    )

    return render(
        request,
        'orders/order_detail.html',
        {
            'order': order
        }
    )


@login_required
def cancel_order(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )
    

    if order.status in [
        'payment Verification',
        'Processing'
    ]:

        order.status = 'Cancelled'

        order.save()

        # Restore Stock

        order_items = OrderItem.objects.filter(
            order=order
        )

        for item in order_items:

            product = item.product

            product.stock += item.quantity

            product.save()

        messages.success(
            request,
            'Order Cancelled Successfully'
        )

    else:

        messages.error(
            request,
            'This order cannot be cancelled'
        )

    return redirect(
        'my_orders'
    )


@login_required
def payment_page(request):
    flow = request.session.get(
        'checkout_type'
    )
    if flow == 'buy_now':

        total = Decimal(
            request.session.get(
                'buy_now_total',
                '0'
            )
        )

    else:

        total = Decimal(
            request.session.get(
                'final_total',
                '0'
            )
        )

    if total <= 0:

        messages.error(
            request,
            "Invalid payment amount."
        )

        return redirect('products')

    upi_link = (
        f"upi://pay?"
        f"pa=9912061912@ptsbi"
        f"&pn=SKSphere"
        f"&am={total}"
        f"&cu=INR"
    )

    qr = qrcode.make(
        upi_link
    )

    buffer = BytesIO()

    qr.save(
        buffer,
        format="PNG"
    )

    qr_base64 = base64.b64encode(
        buffer.getvalue()
    ).decode()

    return render(
        request,
        'orders/payment.html',
        {
            'qr_code': qr_base64,
            'total': total
        }
    )
def send_order_email(order):
    print(order.user.email)
    try:
        send_mail(
            subject=f"Order #{order.id} Confirmed",
            message=f"""
Hello {order.full_name},

Your order has been placed successfully.

Order ID: {order.id}

Total Amount: ₹{order.total_amount}

Thank you for shopping with SKSphere.
""",
            from_email=None,
            recipient_list=[order.user.email],
            fail_silently=False
        )

        print("Email sent successfully")

    except Exception as e:
        print("Email sending failed:", e)


@login_required
def apply_coupon(request):

    if request.method == "POST":

        code = request.POST.get(
            'coupon'
        ).upper()

        cart_items = Cart.objects.filter(
            user=request.user
        )

        total = sum(
            item.product.price * item.quantity
            for item in cart_items
        )

        try:

            coupon = Coupon.objects.get(
                code=code
            )

            if not coupon.is_valid():

                messages.error(
                    request,
                    "Coupon Expired"
                )

            elif total < coupon.minimum_amount:

                messages.error(
                    request,
                    f"Minimum purchase ₹{coupon.minimum_amount}"
                )

            else:

                request.session[
                    'checkout_coupon_id'
                ] = coupon.id

                messages.success(
                    request,
                    "Coupon Applied Successfully!"
                )

        except Coupon.DoesNotExist:

            messages.error(
                request,
                "Invalid Coupon"
            )

    return redirect('checkout')




@login_required
def buy_now(request, product_id):
    
    product = get_object_or_404(
        Product,
        id=product_id
    )

    if product.stock <= 0:

        messages.error(
            request,
            "Product is out of stock."
        )

        return redirect(
            'product_detail',
            product_id=product.id
        )

    request.session['buy_now_product'] = product.id
    request.session['buy_now_qty'] = 1

    request.session.pop(
        'buy_now_coupon_id',
        None
    )

    request.session.pop(
        'buy_now_total',
        None
    )

    return redirect(
        'buy_now_checkout'
    )

@login_required
def buy_now_checkout(request):
    request.session['checkout_type'] = 'buy_now'
    product_id = request.session.get(
        'buy_now_product'
    )

    if not product_id:

        return redirect(
            'products'
        )

    product = get_object_or_404(Product, id=product_id)

    qty = request.session.get(
        'buy_now_qty',
        1
    )

    total = product.price * qty

    discount = 0

    coupon = None

    coupon_id = request.session.get(
        'buy_now_coupon_id'
    )

    if coupon_id:

        try:

            coupon = Coupon.objects.get(
                id=coupon_id
            )

            if coupon.is_valid():

                discount = (
                    total *
                    coupon.discount
                ) / 100

        except Coupon.DoesNotExist:
            request.session.pop(
            'buy_now_coupon_id',
            None
            )

    final_total = total - discount

    request.session[
        'buy_now_total'
    ] = str(final_total)
    request.session.pop(
        'checkout_coupon_id',
        None
    )

    return render(
        request,
        'orders/buy_now_checkout.html',
        {
            'product': product,
            'qty': qty,
            'total': total,
            'discount': discount,
            'final_total': final_total,
            'coupon': coupon
        }
    )

@login_required
def save_buy_now_checkout(request):
    if request.method == "POST":
        request.session['full_name'] = request.POST.get(
            'full_name'
        )

        request.session['address'] = request.POST.get(
            'address'
        )

        request.session['phone'] = request.POST.get(
            'phone'
        )

        request.session['city'] = request.POST.get(
            'city'
        )

        payment_method = request.POST.get(
            'payment_method'
        )

        request.session[
            'buy_now_payment_method'
        ] = payment_method

        if payment_method == 'COD':

            return redirect(
                'place_buy_now_order'
            )
        return redirect(
            'payment'
        )

    return redirect(
        'buy_now_checkout'
    )

@login_required
def buy_now_increase(request):

    qty = request.session.get(
        'buy_now_qty',
        1
    )

    product_id = request.session.get(
        'buy_now_product'
    )

    product = Product.objects.get(
        id=product_id
    )

    if qty < product.stock:

        request.session[
            'buy_now_qty'
        ] = qty + 1

    return redirect(
        'buy_now_checkout'
    )

@login_required
def buy_now_decrease(request):

    qty = request.session.get(
        'buy_now_qty',
        1
    )

    if qty > 1:

        request.session[
            'buy_now_qty'
        ] = qty - 1

    return redirect(
        'buy_now_checkout'
    )


@login_required
def apply_buy_now_coupon(request):

    if request.method == "POST":

        code = request.POST.get(
            'coupon'
        ).strip().upper()

        product_id = request.session.get(
            'buy_now_product'
        )

        if not product_id:

            messages.error(
                request,
                "No product selected."
            )

            return redirect(
                'products'
            )

        product = Product.objects.get(
            id=product_id
        )

        qty = request.session.get(
            'buy_now_qty',
            1
        )

        total = (
            product.price *
            qty
        )

        try:

            coupon = Coupon.objects.get(
                code=code
            )

            if not coupon.is_valid():

                messages.error(
                    request,
                    "Coupon expired."
                )

            elif total < coupon.minimum_amount:

                messages.error(
                    request,
                    f"Minimum purchase ₹{coupon.minimum_amount} required."
                )

            else:

                request.session[
                    'buy_now_coupon_id'
                ] = coupon.id

                messages.success(
                    request,
                    f"{coupon.code} applied successfully!"
                )

        except Coupon.DoesNotExist:

            messages.error(
                request,
                "Invalid coupon code."
            )

    return redirect(
        'buy_now_checkout'
    )

@login_required
def remove_buy_now_coupon(request):

    request.session.pop(
        'buy_now_coupon_id',
        None
    )

    messages.success(
        request,
        "Coupon removed."
    )

    return redirect(
        'buy_now_checkout'
    )

@login_required
def place_buy_now_order(request):

    product_id = request.session.get(
        'buy_now_product'
    )

    qty = request.session.get(
        'buy_now_qty',
        1
    )

    total = Decimal(
        request.session.get(
            'buy_now_total',
            '0'
        )
    )

    product = Product.objects.get(
        id=product_id
    )
    payment_method = request.session.get(
        'buy_now_payment_method'
    )

    if qty > product.stock:

        messages.error(
            request,
            "Not enough stock."
        )

        return redirect(
            'buy_now_checkout'
        )

    order = Order.objects.create(

        user=request.user,

        full_name=request.session.get(
            'full_name'
        ),

        phone=request.session.get(
            'phone'
        ),

        address=request.session.get(
            'address'
        ),

        city=request.session.get(
            'city'
        ),
        payment_method=payment_method,

        total_amount=total,

        status='Payment Verification'
    )

    OrderItem.objects.create(

        order=order,

        product=product,

        quantity=qty,

        price=product.price
    )

    product.stock -= qty
    product.save()

    screenshot = request.FILES.get(
        'screenshot'
    )

    if screenshot:

        Payment.objects.create(
            order=order,
            screenshot=screenshot
        )

    send_order_email(order)

    request.session.pop(
        'buy_now_product',
        None
    )

    request.session.pop(
        'buy_now_qty',
        None
    )

    request.session.pop(
        'buy_now_total',
        None
    )

    request.session.pop(
        'buy_now_coupon_id',
        None
    )

    payment_method = request.session.get(
        'buy_now_payment_method'
    )

    if payment_method == "COD":

        return redirect(
            'order_success'
        )

    return redirect(
        'payment_pending'
    )

@login_required
def order_success(request):

    return render(
        request,
        'orders/order_success.html'
    )