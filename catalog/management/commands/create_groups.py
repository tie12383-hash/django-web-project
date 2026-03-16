from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product

class Command(BaseCommand):
    help = 'Создает группы модераторов и контент-менеджеров с правами'

    def handle(self, *args, **options):
        # Группа модераторов продуктов
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')
        if created:
            self.stdout.write('Группа "Модератор продуктов" создана')
        else:
            self.stdout.write('Группа "Модератор продуктов" уже существует')

        # Получаем content type для продукта
        content_type = ContentType.objects.get_for_model(Product)

        # Право на отмену публикации
        unpublish_perm, _ = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            name='Can unpublish product',
            content_type=content_type,
        )
        # Право на удаление продукта
        delete_perm = Permission.objects.get(
            codename='delete_product',
            content_type=content_type,
        )

        # Добавляем права группе
        moderator_group.permissions.add(unpublish_perm, delete_perm)

        # Группа контент-менеджеров
        content_group, created = Group.objects.get_or_create(name='Контент-менеджер')
        if created:
            self.stdout.write('Группа "Контент-менеджер" создана')
        else:
            self.stdout.write('Группа "Контент-менеджер" уже существует')

        self.stdout.write(self.style.SUCCESS('Группы успешно настроены'))