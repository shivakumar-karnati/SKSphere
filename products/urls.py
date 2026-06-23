from django.urls import path
from .views import home , product_list , product_detail,category_products,wishlist,add_to_wishlist,add_review,dashboard,edit_review,delete_review
urlpatterns = [
    path('', home, name='home'),

    path('all-products/',product_list,name='products'),

    path('product/<int:id>/',product_detail,name='product_detail'),

    path('category/<int:category_id>/',category_products,name='category_products'),
    
    path('wishlist/',wishlist,name='wishlist'),

    path('wishlist/add/<int:product_id>/',add_to_wishlist,name='add_to_wishlist'),

    path('review/<int:product_id>/',add_review,name='add_review'),

    path('review/edit/<int:review_id>/',edit_review,name='edit_review'),

    path('review/delete/<int:review_id>/',delete_review,name='delete_review'),

    path('dashboard/',dashboard,name='dashboard'),
]