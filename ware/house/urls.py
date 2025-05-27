from django.urls import path, include
from . import views


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('<int:id>/', views.invoice, name='invoice'), 
    path('invoice/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('invoice/<int:invoice_id>/pdf/', views.invoice_pdf, name='invoice_pdf'),
]








# Ajit Hanumant Chavan
# Skoy jsminsmy vjsbsm