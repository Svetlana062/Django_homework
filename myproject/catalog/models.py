from django.db import models


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
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """Отображаемое имя модели в единственном и множественном числе."""
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"

    def __str__(self):
        """Строковое представление продукта."""
        return self.name
