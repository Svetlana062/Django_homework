from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import ProductForm
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
        # Получаем данные из формы
        data = form.cleaned_data
        name = data['name']
        phone = data['phone']
        message_text = data['message']

        # Формируем тему и тело письма
        subject = f'Новое сообщение от {name}'
        message_body = f'Имя: {name}\nТелефон: {phone}\n\nСообщение:\n{message_text}'

        # Отправляем письмо
        send_mail(
            subject,
            message_body,
            settings.EMAIL_HOST_USER,  # email-отправитель
            [settings.EMAIL_HOST_USER],  # email получателя писем от пользователей
            fail_silently=False,
        )

        return super().form_valid(form)

    def form_invalid(self, form):
        response =super().form_invalid(form)
        response.context_data['error_message'] = "Пожалуйста, исправьте ошибки в форме."
        return response


class ContactSuccessView(TemplateView):
    template_name = 'catalog/contact_success.html'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('home')


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
