from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView, TemplateView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .forms import ProductForm
from .forms import ContactForm
from .models import Product


class HomeView(ListView):
    """Главная страница каталога, отображает список продуктов."""
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ContactView(FormView):
    """Форма обратной связи для отправки сообщений."""
    template_name = 'catalog/contacts.html'
    form_class = ContactForm
    success_url = reverse_lazy('contact_success')

    def form_valid(self, form):
        """Обработка валидной формы: отправка письма и перенаправление."""
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
        """Обработка невалидной формы: добавление сообщения об ошибке."""
        response =super().form_invalid(form)
        response.context_data['error_message'] = "Пожалуйста, исправьте ошибки в форме."
        return response


class ContactSuccessView(TemplateView):
    """Страница подтверждения успешной отправки сообщения."""
    template_name = 'catalog/contact_success.html'


class ProductDetailView(LoginRequiredMixin, DetailView):
    """Страница с подробным описанием конкретного продукта."""
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        user = self.request.user
        # Проверка: пользователь — владелец или есть разрешение
        product.can_edit = (
                user.is_authenticated and
                (product.owner == user or user.has_perm('catalog.delete_product'))
        )
        context['product'] = product
        return context


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    """Создание нового продукта."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')
    permission_required = 'catalog.add_product'

    def form_valid(self, form):
        # Устанавливаем владельца как текущего пользователя
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    """Редактирование существующего продукта."""
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')
    permission_required = 'catalog.change_product'


class ProductDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    """Удаление продукта."""
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('home')
    permission_required = 'catalog.delete_product'


class ProductListView(ListView):
    """Просмотр списка продуктов."""
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        for product in queryset:
            # Проверка: пользователь — владелец или есть разрешение
            product.can_edit = (
                    user.is_authenticated and
                    (product.owner == user or user.has_perm('catalog.delete_product'))
            )
        return queryset


class ProductUnpublishView(PermissionRequiredMixin, UpdateView):
    """Отмена публикации."""
    model = Product
    fields = []  # или нужные поля для редактирования статуса
    template_name = 'catalog/product_unpublish.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'catalog.can_unpublish_product'

    def form_valid(self, form):
        product = form.save(commit=False)
        product.status = 'unpublished'  # или is_published=False при BooleanField
        product.save()
        return super().form_valid(form)
