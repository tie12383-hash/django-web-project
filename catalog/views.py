from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Product, Category, Contact
from .forms import ContactForm
from django.shortcuts import render, get_object_or_404
from .models import Product
from django.shortcuts import redirect, render
from .forms import ProductForm

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('catalog:home')
    else:
        form = ProductForm()
    context = {'form': form}
    return render(request, 'catalog/product_form.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'catalog/product_detail.html', context)


def home(request):
    product_list = Product.objects.all().order_by('-created_at')
    paginator = Paginator(product_list, 6)  # 6 товаров на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'title': 'Главная',
        'page_obj': page_obj,
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
