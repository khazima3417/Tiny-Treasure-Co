from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('shop/', views.shop_view, name='shop'),
    path('product/<slug:slug>/', views.product_detail_view, name='product_detail'),
    path('customize/', views.customize_view, name='customize'),
    path('cart/', views.cart_checkout_view, name='cart'),
    path('checkout/', views.cart_checkout_view, name='cart_checkout'),
    path('cart/add/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/add-custom/', views.add_custom_box_view, name='add_custom_box'),
    path('cart/update/', views.update_cart_quantity_view, name='update_cart_quantity'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('order/confirmed/<str:order_number>/', views.order_confirmation_view, name='order_confirmation'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
    path('newsletter/', views.newsletter_view, name='newsletter'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('account/', views.profile_view, name='profile'),
]
