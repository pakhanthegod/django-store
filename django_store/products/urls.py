from django.urls import path

from . import views


app_name = 'products'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list_all'),
    path('<slug:category>/', views.ProductListView.as_view(), name='product_list'),
    path('<slug:category>/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('<slug:category>/page<int:page>/', views.ProductListView.as_view(), name='product_list_page'),
]