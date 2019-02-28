from django.urls import path

from . import views


app_name = 'products'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='list_all'),
    path('page-<int:page>/', views.ProductListView.as_view(), name='list_all_page'),
    path('<slug:category>/', views.ProductListView.as_view(), name='list'),
    path('<slug:category>/<int:pk>/', views.ProductDetailView.as_view(), name='detail'),
    path('<slug:category>/page-<int:page>/', views.ProductListView.as_view(), name='list_page'),
]