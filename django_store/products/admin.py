from django.contrib import admin

from .models import Product, Category, Brand


admin.site.register([Product, Category, Brand])
