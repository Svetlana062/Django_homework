from django.urls import path
from django.views.generic import TemplateView

from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contacts, name='contacts'),
    path('contacts/success/', TemplateView.as_view(template_name='catalog/contact_success.html'), name='contact_success'),
]
