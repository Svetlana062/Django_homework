from django.db import models
from django.urls import reverse


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое')
    preview_image = models.ImageField(upload_to='previews/', verbose_name='Превью', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания') # автоматическое заполнение
    is_published = models.BooleanField(default=False, verbose_name='Опубликовать') # признак публикации (булевое поле)
    views_count = models.PositiveIntegerField(default=0, verbose_name='Количество просмотров') # (автоматическое заполнение)

    class Meta:
        verbose_name = 'Блоговая запись'
        verbose_name_plural = 'Блоговые записи'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Метод для автоматического получения URL объекта."""
        return reverse('blog:detail', kwargs={'pk': self.pk})
