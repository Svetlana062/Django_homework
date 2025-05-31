from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from .views import (
    HomeView,
    ContactView,
    ContactSuccessView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductListView,
)


urlpatterns = [
    # Публичные
    path('', HomeView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('contacts/success/', ContactSuccessView.as_view(), name='contact_success'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/list/', ProductListView.as_view(), name='product_list'),

    # Для просмотра нужна авторизация
    path('product/add/', ProductCreateView.as_view(), name='product_add'),
    path('product/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
]

# Обслуживание медиафайлов при DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
