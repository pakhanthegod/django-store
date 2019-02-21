from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('profiles/', include('profiles.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)