from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, TemplateView, DetailView

from .forms import ContactForm
from .models import Product


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ContactView(FormView):
    template_name = 'catalog/contacts.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_success')

    def form_valid(self, form):
        print(form.cleaned_data) # для теста
        return super().form_valid(form)

    def form_invalid(self, form):
        response =super().form_invalid(form)
        response.context_data['error_message'] = "Пожалуйста, исправьте ошибки в форме."
        return response


class ContactSuccessView(TemplateView):
    template_name = 'catalog/contact_success.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'
