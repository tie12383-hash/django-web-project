import os
from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product, Contact
from decimal import Decimal
from django.utils import timezone


class Command(BaseCommand):
    help = 'Загружает тестовые данные в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Удалить все существующие данные перед загрузкой'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Удаление существующих данных...')
            Product.objects.all().delete()
            Category.objects.all().delete()
            Contact.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('Все данные удалены'))

        self.stdout.write('Создание тестовых категорий...')
        categories_data = [
            {'name': 'Электроника', 'description': 'Техника и гаджеты'},
            {'name': 'Одежда', 'description': 'Мужская и женская одежда'},
            {'name': 'Книги', 'description': 'Художественная и учебная литература'},
            {'name': 'Мебель', 'description': 'Домашняя и офисная мебель'},
            {'name': 'Спорт', 'description': 'Спортивные товары и инвентарь'},
        ]

        categories = {}
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            categories[cat_data['name']] = category
            if created:
                self.stdout.write(f'Создана категория: {cat_data["name"]}')

        self.stdout.write('Создание тестовых продуктов...')
        products_data = [
            {
                'name': 'Смартфон iPhone 14',
                'description': 'Новейший смартфон Apple с камерой 48 МП',
                'price': Decimal('89990.00'),
                'category': categories['Электроника'],
            },
            {
                'name': 'Ноутбук MacBook Pro',
                'description': 'Мощный ноутбук для работы и творчества',
                'price': Decimal('149990.00'),
                'category': categories['Электроника'],
            },
            {
                'name': 'Футболка мужская',
                'description': 'Хлопковая футболка, 100% хлопок',
                'price': Decimal('1990.00'),
                'category': categories['Одежда'],
            },
            {
                'name': 'Джинсы',
                'description': 'Прямые джинсы классического кроя',
                'price': Decimal('4990.00'),
                'category': categories['Одежда'],
            },
            {
                'name': 'Война и мир',
                'description': 'Роман Льва Толстого в 4 томах',
                'price': Decimal('2990.00'),
                'category': categories['Книги'],
            },
            {
                'name': 'Диван угловой',
                'description': 'Угловой диван с механизмом трансформации',
                'price': Decimal('45990.00'),
                'category': categories['Мебель'],
            },
            {
                'name': 'Велотренажер',
                'description': 'Магнитный велотренажер с компьютером',
                'price': Decimal('15990.00'),
                'category': categories['Спорт'],
            },
            {
                'name': 'Баскетбольный мяч',
                'description': 'Официальный размер 7, резиновое покрытие',
                'price': Decimal('2490.00'),
                'category': categories['Спорт'],
            },
        ]

        for prod_data in products_data:
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults=prod_data
            )
            if created:
                self.stdout.write(f'Создан продукт: {prod_data["name"]}')

        self.stdout.write('Создание тестовых контактов...')
        contacts_data = [
            {
                'name': 'Основной офис',
                'email': 'info@example.com',
                'phone': '+7 (999) 123-45-67',
                'address': 'г. Москва, ул. Примерная, д. 123, офис 456',
                'working_hours': 'Пн-Пт: 9:00-18:00, Сб: 10:00-16:00',
                'description': 'Основной офис компании. Принимаем посетителей по предварительной записи.',
            },
            {
                'name': 'Склад и пункт выдачи',
                'email': 'warehouse@example.com',
                'phone': '+7 (999) 987-65-43',
                'address': 'г. Москва, ул. Складская, д. 45, стр. 1',
                'working_hours': 'Пн-Сб: 8:00-20:00',
                'description': 'Склад и пункт самовывоза. Бесплатная парковка для клиентов.',
            },
            {
                'name': 'Техническая поддержка',
                'email': 'support@example.com',
                'phone': '+7 (800) 123-45-67',
                'address': '',
                'working_hours': 'Круглосуточно',
                'description': 'Техническая поддержка по телефону и email.',
            },
        ]

        for contact_data in contacts_data:
            contact, created = Contact.objects.get_or_create(
                name=contact_data['name'],
                defaults=contact_data
            )
            if created:
                self.stdout.write(f'Создан контакт: {contact_data["name"]}')

        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно загружены!'))
