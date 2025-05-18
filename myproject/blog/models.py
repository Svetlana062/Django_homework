from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200) # заголовок
    content = models.TextField() # содержимое
    preview_image = models.ImageField(upload_to='previews/') # превью (изображение)
    created_at = models.DateTimeField(auto_now_add=True) # дата создания
    is_published = models.BooleanField(default=False) # признак публикации (булевое поле)
    views_count = models.PositiveIntegerField(default=0) # количество просмотров

    def __str__(self):
        return self.title
