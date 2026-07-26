from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.contrib.auth import login , logout
from django.contrib.auth.decorators import login_required
from products.models import Wishlist,Review
from orders.models import Order
from django.db.models import Sum
from cart.models import Cart
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.core.mail import send_mail
import random
from time import time

def register(request):

    if request.method == "POST":

        username = request.POST['username'].strip()
        email = request.POST['email'].strip().lower()
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:

            return render(
                request,
                'accounts/register.html',
                {
                    'error': 'Passwords do not match'
                }
            )

        if User.objects.filter(username=username).exists():

            return render(
                request,
                'accounts/register.html',
                {
                    'error': 'Username already exists'
                }
            )

        if User.objects.filter(email=email).exists():

            return render(
                request,
                'accounts/register.html',
                {
                    'error': 'Email already exists'
                }
            )

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('login')

    return render(
        request,
        'accounts/register.html'
    )

def user_login(request):

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(
                request,
                user
            )

            return redirect('home')

        else:

            return render(
                request,
                'accounts/login.html',
                {
                    'error':'Invalid Username or Password'
                }
            )

    return render(
        request,
        'accounts/login.html'
    )

def user_logout(request):
    logout(request)

    return redirect('home')

@login_required
def profile(request):


    profile = request.user.profile

    wishlist_count = Wishlist.objects.filter(
        user=request.user
    ).count()

    cart_count = Cart.objects.filter(
        user=request.user
    ).count()

    order_count = Order.objects.filter(
        user=request.user
    ).count()

    review_count = Review.objects.filter(
        user=request.user
    ).count()
    total_spend = Order.objects.filter(
            user=request.user,
            status='Delivered'
        ).aggregate(
            total=Sum('total_amount')
        )['total'] or 0

    recent_orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]

    return render(
        request,
        'accounts/profile.html',
        {
            'profile': profile,
            'wishlist_count': wishlist_count,
            'cart_count': cart_count,
            'order_count': order_count,
            'total_spend': total_spend,
            'review_count': review_count,
            'recent_orders': recent_orders,
        }
    )


@login_required
def edit_profile(request):


    profile = request.user.profile

    if request.method == 'POST':

        request.user.username = request.POST.get(
            'username'
        )

        request.user.email = request.POST.get(
            'email'
        )

        profile.phone = request.POST.get(
            'phone'
        )

        profile.city = request.POST.get(
            'city'
        )

        profile.bio = request.POST.get(
            'bio'
        )

        profile.address = request.POST.get(
            'address'
        )

        if request.FILES.get('profile_pic'):

            profile.profile_pic = request.FILES.get(
                'profile_pic'
            )
        
        new_username = request.POST.get('username')

        if User.objects.exclude(
                id=request.user.id
        ).filter(
                username=new_username
        ).exists():

            messages.error(
                request,
                "Username already taken"
            )

            return redirect(
                'edit_profile'
            )
        
        new_email = request.POST.get('email')

        if User.objects.exclude(
                id=request.user.id
        ).filter(
                email=new_email
        ).exists():

            messages.error(
                request,
                "email already taken"
            )

            return redirect(
                'edit_profile'
            )

        request.user.save()
        profile.save()

        messages.success(
            request,
            'Profile Updated Successfully'
        )

        return redirect('profile')

    return render(
        request,
        'accounts/edit_profile.html',
        {
            'profile': profile
        }
    )



@login_required
def change_password(request):

    if request.method == 'POST':

        form = PasswordChangeForm(
            request.user,
            request.POST
        )

        if form.is_valid():

            user = form.save()
            try:
                send_mail(
                        "Password Changed",

                        """
                    Your SKSphere password was changed successfully.

                    If this wasn't you, contact support immediately.
                    """,

                        None,

                        [user.email]
                    )
            except Exception as e:
                print("Email sending failed:", e)

            update_session_auth_hash(
                request,
                user
            )

            messages.success(
                request,
                'Password changed successfully!'
            )

            return redirect(
                'profile'
            )

    else:

        form = PasswordChangeForm(
            request.user
        )

    return render(
        request,
        'accounts/change_password.html',
        {
            'form': form
        }
    )


def forgot_password(request):
    
    step = request.session.get(
            "reset_step",
            "email"
        )

    if request.method == "POST":

        action = request.POST.get("action")

        # ==================================
        # STEP 1 : SEND OTP
        # ==================================

        if action == "send_otp":

            email = request.POST.get(
                "email"
            ).strip().lower()

            try:

                User.objects.get(
                    email=email
                )

                otp = str(
                    random.randint(
                        100000,
                        999999
                    )
                )

                request.session["reset_email"] = email
                request.session["reset_otp"] = otp
                request.session["otp_time"] = int(time())
                request.session["reset_step"] = "otp"
                try:
                    send_mail(
                        "SKSphere Password Reset OTP",
                        f"""
                    Your OTP is: {otp}

                    This OTP is valid for 5 minutes.

                    Do not share this OTP with anyone.
                                        """,
                        None,
                        [email]
                    )
                except Exception as e:
                    print("Email sending failed:", e)

                messages.success(
                    request,
                    "OTP sent successfully. Check Inbox or Spam folder."
                )

                return redirect(
                    "forgot_password"
                )

            except User.DoesNotExist:

                messages.error(
                    request,
                    "No account found with this email."
                )

                return redirect(
                    "forgot_password"
                )
        elif action == "resend_otp":

            email = request.session.get("reset_email")

            if email:

                otp = str(
                    random.randint(
                        100000,
                        999999
                    )
                )

                request.session["reset_otp"] = otp
                request.session["otp_time"] = int(time())
                request.session["reset_step"] = "otp"
                try:
                    send_mail(
                        "SKSphere Password Reset OTP",
                        f"""
                        Your new OTP is: {otp}

                        This OTP is valid for 5 minutes.
                                    """,
                        None,
                        [email]
                    )
                except Exception as e:
                    print("Email sending failed:", e)
                messages.success(
                    request,
                    "New OTP sent successfully."
                )

            return redirect(
                "forgot_password"
            )
        # ==================================
        # STEP 2 : VERIFY OTP
        # ==================================

        elif action == "verify_otp":

            entered_otp = request.POST.get(
                "otp"
            )

            saved_otp = request.session.get(
                "reset_otp"
            )

            otp_time = request.session.get(
                "otp_time"
            )

            if not saved_otp or not otp_time:

                messages.error(
                    request,
                    "OTP expired. Request a new OTP."
                )

                request.session["reset_step"] = "email"

                return redirect(
                    "forgot_password"
                )

            if int(time()) - otp_time > 100:

                request.session.pop(
                    "reset_otp",
                    None
                )

                request.session.pop(
                    "otp_time",
                    None
                )

                request.session.pop(
                    "reset_email",
                    None
                )

                request.session["reset_step"] = "email"
                messages.error(
                    request,
                    "OTP expired. Request a new OTP."
                )

                return redirect(
                    "forgot_password"
                )

            if entered_otp != saved_otp:

                messages.error(
                    request,
                    "Invalid OTP."
                )

                return redirect(
                    "forgot_password"
                )

            request.session["reset_step"] = "password"

            messages.success(
                request,
                "OTP verified successfully."
            )
            request.session["otp_verified"] = True
            return redirect(
                "forgot_password"
            )
        
        # ==================================
        # STEP 3 : RESET PASSWORD
        # ==================================

        elif action == "reset_password":

            if request.session.get(
                "reset_step"
            ) != "password":

                messages.error(
                    request,
                    "OTP verification required."
                )

                return redirect(
                    "forgot_password"
                )

            password1 = request.POST.get(
                "password1"
            )

            password2 = request.POST.get(
                "password2"
            )

            if password1 != password2:

                messages.error(
                    request,
                    "Passwords do not match."
                )

                return redirect(
                    "forgot_password"
                )

            email = request.session.get(
                "reset_email"
            )

            try:

                user = User.objects.get(
                    email=email
                )

                user.set_password(
                    password1
                )

                user.save()
                try:
                    send_mail(
                        "Password Changed Successfully",
                        """
                        Your SKSphere password has been changed.

                        If this wasn't you, contact support immediately.
                        """,
                        None,
                        [user.email]
                    )
                except Exception as e:
                    print("Email sending failed:", e)
                request.session.pop(
                    "reset_email",
                    None
                )

                request.session.pop(
                    "reset_otp",
                    None
                )

                request.session.pop(
                    "otp_time",
                    None
                )

                request.session.pop(
                    "reset_step",
                    None
                )

                messages.success(
                    request,
                    "Password reset successfully."
                )

                return redirect(
                    "login"
                )

            except User.DoesNotExist:

                messages.error(
                    request,
                    "User not found."
                )

                return redirect(
                    "forgot_password"
                )
    remaining_time = 0
    otp_time = request.session.get("otp_time")

    if otp_time:

        if int(time()) - otp_time > 100:

            request.session.pop(
                "reset_email",
                None
            )

            request.session.pop(
                "reset_otp",
                None
            )

            request.session.pop(
                "otp_time",
                None
            )

            request.session["reset_step"] = "email"

            step = "email"

            messages.error(
                request,
                "OTP expired. Please request a new OTP."
            )

    step = request.session.get(
        "reset_step",
        "email"
    )
    return render(
        request,
        "accounts/forgot_password.html",
        {
            "step": step,
            "remaining_time": remaining_time
        }
    )