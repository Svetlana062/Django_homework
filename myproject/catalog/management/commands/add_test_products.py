import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

# Импортируем модели из приложения catalog
from catalog.models import Product, Category


class Command(BaseCommand):
    """Кастомная команда."""
    help = 'Загрузить тестовые данные в базу данных'

    def handle(self, *args, **kwargs):
        """Кастомная команда для удаления и добавления тестовых продуктов."""
        # Удаляем существующие данные перед загрузкой новых данных.
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Загружаем фиктуры.
        fixture_path = os.path.join(settings.BASE_DIR, 'category_fixture.json')  # Путь к фиктуре

        try:
            call_command('loaddata', fixture_path)
            self.stdout.write(self.style.SUCCESS('Тестовые данные успешно загружены!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при загрузке данных: {e}'))
