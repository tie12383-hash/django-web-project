from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import ContactForm


def home(request):
    """Контроллер для главной страницы"""
    context = {
        'title': 'Главная',
        'products': [
            {
                'name': 'Товар 1',
                'price': '$100',
                'features': [
                    '10 пользователей',
                    '2 GB хранилища',
                    'Email поддержка',
                    'Help center access'
                ]
            },
            {
                'name': 'Товар 2',
                'price': '$200',
                'features': [
                    '20 пользователей',
                    '5 GB хранилища',
                    'Приоритетная поддержка',
                    'Расширенная помощь'
                ]
            },
            {
                'name': 'Товар 3',
                'price': '$300',
                'features': [
                    'Безлимитные пользователи',
                    '10 GB хранилища',
                    '24/7 поддержка',
                    'Персональный менеджер'
                ]
            }
        ]
    }
    return render(request, 'catalog/home.html', context)


def contacts(request):
    """Контроллер для страницы контактов"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Здесь можно добавить логику обработки формы
            # Например, отправка email или сохранение в базу данных
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            telegram = form.cleaned_data['telegram']
            message = form.cleaned_data['message']

            # Выводим данные в консоль (как требовалось в задании)
            print("\n" + "=" * 50)
            print("ДАННЫЕ ФОРМЫ ОБРАТНОЙ СВЯЗИ:")
            print("=" * 50)
            print(f"Имя: {name}")
            print(f"Email: {email}")
            print(f"Telegram: {telegram}")
            print(f"Сообщение: {message}")
            print("=" * 50 + "\n")

            # Добавляем сообщение об успехе
            context = {
                'title': 'Контакты',
                'form': form,
                'success_message': 'Спасибо за ваше сообщение! Мы свяжемся с вами в ближайшее время.'
            }
            return render(request, 'catalog/contacts.html', context)
    else:
        form = ContactForm()

    context = {
        'title': 'Контакты',
        'form': form
    }
    return render(request, 'catalog/contacts.html', context)
