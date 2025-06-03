from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from myproject.catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группу Модератор продуктов и назначает ей права'

    def handle(self, *args, **kwargs):
        group_name = 'Product Moderator'
        group, created = Group.objects.get_or_create(name=group_name)

        # Получаем нужные разрешения
        content_type = ContentType.objects.get_for_model(Product)

        perms_codenames = ['can_unpublish_product', 'can_delete_any_product']
        perms = Permission.objects.filter(codename__in=perms_codenames, content_type=content_type)

        for perm in perms:
            group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS(f'Группа "{group_name}" создана и права назначены'))
