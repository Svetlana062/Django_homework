from django.db import models
from django.conf import settings


class Category(models.Model):
    """Модель категории."""
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        """Отображаемое имя модели в единственном и множественном числе."""
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        """Строковое представление категории."""
        return self.name


class Product(models.Model):
    """Модель продукта."""
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('published', 'Опубликован'),
        ('unpublished', 'Отменен публикация'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2) # Цена продукта
    created_at = models.DateTimeField(auto_now_add=True) # Дата создания продукта
    updated_at = models.DateTimeField(auto_now=True) # Дата обновления продукта
    category = models.ForeignKey('catalog.Category', on_delete=models.CASCADE)

    # Поле статуса публикации
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='Статус публикации'
    )

    # Поле владельца
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products',
        verbose_name='Владелец'
    )

    class Meta:
        """Отображаемое имя модели в единственном и множественном числе."""
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

        permissions = [
            ('can_unpublish_product', 'Can unpublish product'), # Может отменять публикацию продукта
            ('can_delete_any_product', 'Can delete any product'), # Может удалять любой продукт
        ]

    def __str__(self):
        """Строковое представление продукта."""
        return self.name
