from django.contrib import admin

from .models import User, Customer


admin.site.register([User, Customer])