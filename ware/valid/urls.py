from django.urls import path, include
from . import views


urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('lll/', views.logout_user, name='logout_user'),
]
