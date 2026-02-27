from django.contrib import admin
from .models import Category, Product, Contact

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'description')
    list_filter = ('created_at', 'updated_at')
    ordering = ('name',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'category', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    list_filter = ('category', 'created_at', 'updated_at')
    search_fields = ('name', 'description')
    filter_horizontal = ()
    ordering = ('-created_at',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'description', 'category', 'price')
        }),
        ('Изображение', {
            'fields': ('image',),
            'classes': ('wide',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'is_active', 'created_at')
    list_display_links = ('id', 'name')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'email', 'phone', 'address')
    ordering = ('name',)
    fieldsets = (
        ('Контактная информация', {
            'fields': ('name', 'email', 'phone', 'address', 'working_hours')
        }),
        ('Дополнительная информация', {
            'fields': ('description', 'is_active')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
