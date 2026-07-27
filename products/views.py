from django.shortcuts import render,redirect,get_object_or_404
from .models import Product,Category,Wishlist,Review
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.contrib.auth.models import User
from django.contrib import messages
from orders.models import Order,OrderItem
from django.db.models import Sum
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import time

from django.conf import settings
from django.db.models.functions import TruncMonth
from django.contrib.admin.views.decorators import staff_member_required

def home(request):

    categories = Category.objects.all()

    featured_products = Product.objects.order_by(
        '-created_at'
    )[:8]

    new_arrivals = Product.objects.order_by(
        '-created_at'
    )[:8]

    best_sellers = Product.objects.order_by(
        '-sold_count'
    )[:8]

    recent_ids = request.session.get(
        'recent_products',
        []
    )

    recent_products = Product.objects.filter(
        id__in=recent_ids
    )

    recommended_products = Product.objects.exclude(
        id__in=recent_ids
    ).order_by('?')[:8]

    return render(
        request,
        'products/home.html',
        {
            'categories': categories,
            'featured_products': featured_products,
            'new_arrivals': new_arrivals,
            'best_sellers': best_sellers,
            'recent_products': recent_products,
            'recommended_products': recommended_products,
        }
    )


def product_list(request):

    products = Product.objects.all()

    categories = Category.objects.all()

    query = request.GET.get('q')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    category_id = request.GET.get('category')

    if category_id:
        products = products.filter(
            category_id=category_id
        )

    price = request.GET.get('price')

    if price == '1':
        products = products.filter(price__lt=500)

    elif price == '2':
        products = products.filter(
            price__gte=500,
            price__lte=2000
        )

    elif price == '3':
        products = products.filter(price__gt=2000)

    sort = request.GET.get('sort')

    if sort == 'low':
        products = products.order_by('price')

    elif sort == 'high':
        products = products.order_by('-price')

    elif sort == 'new':
        products = products.order_by('-created_at')



    return render(
        request,
        'products/product_list.html',
        {
            'products': products,
            'categories': categories
        }
    )

def product_detail(request, id):

    product = get_object_or_404(Product, id=id) 

    recent_products = request.session.get( 'recent_products', [] ) 
    
    if product.id in recent_products: 
        recent_products.remove(product.id) 
        recent_products.insert( 0, product.id )

    recent_products = recent_products[:8] 

    request.session[ 'recent_products' ] = recent_products

    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        id=product.id
    )[:4]

    purchased = False

    if request.user.is_authenticated:

        purchased = OrderItem.objects.filter(

            order__user=request.user,

            order__status='Delivered',

            product=product

        ).exists()

    reviews = Review.objects.filter(
            product=product
        ).order_by('-created_at')
    average_rating = Review.objects.filter(
        product=product
    ).aggregate(
        Avg('rating')
    )['rating__avg']

    return render(
        request,
        'products/product_detail.html',
        {
            'product': product,
            'related_products': related_products,
            'reviews': reviews,
            'average_rating': average_rating,
            'purchased': purchased,
        }
    )
def category_products(request, category_id):

    category = Category.objects.get(
        id=category_id
    )

    products = Product.objects.filter(
        category=category
    )

    categories = Category.objects.all()

    query = request.GET.get('q')

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    price = request.GET.get('price')

    if price == '1':
        products = products.filter(
            price__lt=500
        )

    elif price == '2':
        products = products.filter(
            price__gte=500,
            price__lte=2000
        )

    elif price == '3':
        products = products.filter(
            price__gt=2000
        )

    sort = request.GET.get('sort')

    if sort == 'low':
        products = products.order_by('price')

    elif sort == 'high':
        products = products.order_by('-price')

    elif sort == 'new':
        products = products.order_by('-created_at')

    return render(
        request,
        'products/category_products.html',
        {
            'products': products,
            'categories': categories,
            'category': category,
            'current_category': category,  
        }
    )
@login_required
def add_to_wishlist(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if created:
        messages.success(request, "Added to wishlist")
    else:
        messages.info(request, "Already in wishlist")

    return redirect(
        'wishlist'
    )

@login_required
def wishlist(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    )

    return render(
        request,
        'products/wishlist.html',
        {
            'wishlist_items': wishlist_items
        }
    )


@login_required
def add_review(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    purchased = OrderItem.objects.filter(

        order__user=request.user,

        order__status='Delivered',

        product=product

    ).exists()

    if not purchased:

        messages.error(
            request,
            "You can review only purchased products."
        )

        return redirect(
            'product_detail',
            id=product_id
        )

    review_exists = Review.objects.filter(

        user=request.user,

        product=product

    ).exists()

    if review_exists:

        messages.warning(
            request,
            "You already reviewed this product. Edit your review instead."
        )

        return redirect(
            'product_detail',
            id=product_id
        )

    if request.method == "POST":

        Review.objects.create(

            product=product,

            user=request.user,

            rating=request.POST.get('rating'),

            comment=request.POST.get('comment')

        )

        messages.success(
            request,
            "Review added successfully."
        )

    return redirect(
        'product_detail',
        id=product_id
    )

@login_required
def edit_review(request, review_id):

    review = get_object_or_404(

        Review,

        id=review_id,

        user=request.user

    )

    if request.method == "POST":

        review.rating = request.POST.get(
            'rating'
        )

        review.comment = request.POST.get(
            'comment'
        )

        review.save()

        messages.success(
            request,
            "Review updated successfully."
        )

        return redirect(
            'product_detail',
            id=review.product.id
        )

    return render(

        request,

        'products/edit_review.html',

        {
            'review': review
        }

    )

@login_required
def delete_review(request, review_id):

    review = get_object_or_404(

        Review,

        id=review_id,

        user=request.user

    )

    product_id = review.product.id

    review.delete()

    messages.success(

        request,

        "Review deleted successfully."

    )

    return redirect(
        'product_detail',
        id=product_id
    )

@staff_member_required
def dashboard(request):
    admin_user = request.user
    total_products = Product.objects.count()

    total_users = User.objects.count()

    total_orders = Order.objects.count()

    total_revenue = (
        Order.objects.aggregate(
            Sum('total_amount')
        )['total_amount__sum']
        or 0
    )

    pending_orders = Order.objects.filter(
        status='Payment Verification'
    ).count()
    processing_orders = Order.objects.filter(
        status='Processing'
    ).count()
    shipped_orders = Order.objects.filter(
        status='Shipped'
    ).count()
    delivered_orders = Order.objects.filter(
        status='Delivered'
    ).count()
    cancelled_orders = Order.objects.filter(
        status='Cancelled'
    ).count()

    recent_orders = Order.objects.order_by(
        '-created_at'
    )[:5]
    recent_reviews = Review.objects.order_by(
        '-created_at'
    )[:5]
    low_stock_products = Product.objects.filter(
        stock__lte=5
    )

    out_of_stock_products = Product.objects.filter(
        stock=0
    )

    monthly_sales = (
        Order.objects
        .filter(status='Delivered')
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(total=Sum('total_amount'))
        .order_by('month')
    )

    months = []
    sales = []

    for item in monthly_sales:

        months.append(
            item['month'].strftime('%b')
        )

        sales.append(
            float(item['total'])
        )

    plt.figure(figsize=(8,4))

    plt.plot(
        months,
        sales,
        marker='o'
    )

    plt.title("Monthly Sales")

    plt.xlabel("Month")

    plt.ylabel("Revenue")

    chart_path = os.path.join(settings.MEDIA_ROOT, 'sales_chart.png')

    plt.savefig(chart_path)
    plt.close('all')

    chart_url = '/media/sales_chart.png?v=' + str(int(time.time()))


    top_products = (

        OrderItem.objects

        .values(
            'product__name'
        )

        .annotate(
            sold=Sum('quantity')
        )

        .order_by('-sold')[:5]
    )

    return render(
        request,
        'products/dashboard.html',
        {
            'admin_user': admin_user,
            'total_products': total_products,
            'total_users': total_users,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'pending_orders': pending_orders,
            'processing_orders': processing_orders,
            'shipped_orders': shipped_orders,
            'delivered_orders': delivered_orders,
            'cancelled_orders': cancelled_orders,
            'recent_orders': recent_orders,
            'recent_reviews': recent_reviews,
            'low_stock_products': low_stock_products,
            'out_of_stock_products': out_of_stock_products,
            'chart_url': chart_url,
            'top_products': top_products,
        }
    )