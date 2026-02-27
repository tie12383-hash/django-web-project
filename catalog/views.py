from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Product, Category, Contact
from .forms import ContactForm


def home(request):
    """Контроллер для главной страницы"""
    latest_products = Product.objects.all().order_by('-created_at')[:5]

    print("\n" + "=" * 60)
    print("ПОСЛЕДНИЕ 5 СОЗДАННЫХ ПРОДУКТОВ:")
    print("=" * 60)
    for product in latest_products:
        print(f"Название: {product.name}")
        print(f"Категория: {product.category}")
        print(f"Цена: {product.price}")
        print(f"Дата создания: {product.created_at}")
        print("-" * 40)
    print("=" * 60 + "\n")

    context = {
        'title': 'Главная',
        'latest_products': latest_products,
        'categories': Category.objects.all()[:4],
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    """Контроллер для страницы контактов"""
    contact_info = Contact.objects.filter(is_active=True)

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            telegram = form.cleaned_data['telegram']
            message = form.cleaned_data['message']

            print("\n" + "=" * 50)
            print("ДАННЫЕ ФОРМЫ ОБРАТНОЙ СВЯЗИ:")
            print("=" * 50)
            print(f"Имя: {name}")
            print(f"Email: {email}")
            print(f"Telegram: {telegram}")
            print(f"Сообщение: {message}")
            print("=" * 50 + "\n")

            context = {
                'title': 'Контакты',
                'form': form,
                'contact_info': contact_info,
                'success_message': 'Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.'
            }
            return render(request, 'catalog/contacts.html', context)
    else:
        form = ContactForm()

    context = {
        'title': 'Контакты',
        'form': form,
        'contact_info': contact_info
    }
    return render(request, 'catalog/contacts.html', context)


def category_products(request, category_id):
    """Контроллер для отображения товаров по категории"""
    category = Category.objects.get(id=category_id)
    products = Product.objects.filter(category=category)

    context = {
        'title': f'Категория: {category.name}',
        'category': category,
        'products': products
    }
    return render(request, 'catalog/category_products.html', context)
