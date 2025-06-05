from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost
from .forms import BlogPostForm


class BlogListView(ListView):
    """Список опубликованных статей."""
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Проверяем, входит ли пользователь в группу 'Content Manager'
        context['is_content_manager'] = user.is_authenticated and user.groups.filter(name='Content Manager').exists()
        return context

    def get_queryset(self):
        """Фильтрация опубликованных статей."""
        return super().get_queryset().filter(is_published=True).order_by('-created_at')


class BlogDetailView(DetailView):
    """Детальный просмотр статьи с увеличением счетчика просмотров."""
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # увеличиваем счетчик просмотров при каждом открытии страницы
        obj.views_count += 1
        obj.save(update_fields=['views_count'])
        # проверка достижения 100 просмотров для отправки письма
        if obj.views_count == 100:
            send_mail(
                'Поздравляем! Статья достигла 100 просмотров',
                f'Статья "{obj.title}" достигла отметки в 100 просмотров.',
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
            )
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        # Проверяем, входит ли пользователь в группу 'Content Manager'
        context['is_content_manager'] = user.is_authenticated and user.groups.filter(name='Content Manager').exists()
        return context


class UserIsContentManagerMixin(UserPassesTestMixin):
    """Миксин для проверки, что пользователь — контент-менеджер."""
    def test_func(self):
        return self.request.user.groups.filter(name='Content Manager').exists()


class BlogCreateView(LoginRequiredMixin, UserIsContentManagerMixin, CreateView):
    """Создание новой статьи."""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blog_form.html'
    success_url = reverse_lazy('blog:list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Создать'
        return context

    def form_valid(self, form):
        action = self.request.POST.get('action')
        if action == 'save_draft':
            form.instance.is_published = False
        elif action == 'publish':
            form.instance.is_published = True
        return super().form_valid(form)


class BlogUpdateView(LoginRequiredMixin, UserIsContentManagerMixin,UpdateView):
    """Редактирование статьи с перенаправлением на просмотр после успешного редактирования."""
    model = BlogPost
    form_class = BlogPostForm
    template_name = 'blog/blog_form.html'

    def get_success_url(self):
        """Перенаправление на страницу просмотра редактируемой статьи после сохранения."""
        return reverse('blog:detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['action'] = 'Редактировать'
        return context


class BlogDeleteView(LoginRequiredMixin, UserIsContentManagerMixin, DeleteView):
    """Удаление статьи."""
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'
    success_url = reverse_lazy('blog:list')
