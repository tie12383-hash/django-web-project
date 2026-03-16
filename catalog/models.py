from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название категории',
        help_text='Введите название категории'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
        help_text='Введите описание категории'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего изменения'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование',
        help_text='Введите наименование товара'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
        help_text='Введите описание товара'
    )
    image = models.ImageField(
        upload_to='products/',
        verbose_name='Изображение',
        blank=True,
        null=True,
        help_text='Загрузите изображение товара'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        verbose_name='Категория',
        help_text='Выберите категорию товара'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Цена за покупку',
        help_text='Введите цену товара'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего изменения'
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name='Опубликовано'
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name='Владелец',
        null=True,  # временно для совместимости, можно сделать обязательным позже
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ['-created_at']
        permissions = [
            ("can_unpublish_product", "Can unpublish product"),
        ]

    def __str__(self):
        return f'{self.name} - {self.price} руб.'


class Contact(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name='Название',
        help_text='Название контактной информации (например, Основной офис)'
    )
    email = models.EmailField(
        verbose_name='Email',
        help_text='Email для связи'
    )
    phone = models.CharField(
        max_length=20,
        verbose_name='Телефон',
        help_text='Номер телефона'
    )
    address = models.TextField(
        verbose_name='Адрес',
        help_text='Физический адрес'
    )
    working_hours = models.CharField(
        max_length=100,
        verbose_name='Часы работы',
        help_text='Часы работы организации'
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
        help_text='Дополнительная информация'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата последнего изменения'
    )

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ['name']

    def __str__(self):
        return self.name
