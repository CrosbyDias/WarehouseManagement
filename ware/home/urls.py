from django.urls import path, include
from .views import *
urlpatterns = [
    # path('admin/', admin.site.urls),
    path('home/', home, name='home'),
    path('add/', add, name='add'),
    path('edit/<int:id>/', edit, name='edit'),
    path('generate/<int:id>/', generate, name='generate'),
    path('delete/<int:id>/', delete, name='delete'),
    # path('search/', search, name='search'),
]