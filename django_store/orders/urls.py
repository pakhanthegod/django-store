from django.urls import path

from . import views


app_name = 'orders'
urlpatterns = [
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/<int:product_id>/', views.AddToCart.as_view(), name='add_to_cart'),
    path('cart/delete/<int:product_id>/', views.DeleteFromCart.as_view(), name='delete_from_cart'),
    path('create/', views.CreateOrderView.as_view(), name='create_order')
]