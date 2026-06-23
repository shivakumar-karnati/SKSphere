from .models import Cart

def cart_count(request):

    count = 0

    if request.user.is_authenticated:

        count = Cart.objects.filter(
            user=request.user
        ).count()

    return {
        'cart_count': count
    }