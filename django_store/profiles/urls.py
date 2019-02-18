from django.urls import path
from django.conf import settings

from . import views


app_name = 'profiles'
urlpatterns = [
    path('signup/', views.UserCreate.as_view(), name='signup'),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('logout/', views.UserLogout.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]