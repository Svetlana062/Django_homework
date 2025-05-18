from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import HomeView, ContactView, ContactSuccessView, ProductDetailView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('contacts/success/', ContactSuccessView.as_view(), name='contact_success'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
