from django import forms
from django.core.exceptions import ValidationError
from .models import Product

# Список запрещенных слов
FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизация полей через Bootstrap
        for field_name, field in self.fields.items():
            if field_name == 'is_published':
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})
        # Для поля категории добавим класс form-select
        self.fields['category'].widget.attrs.update({'class': 'form-select'})
        # Для поля изображения
        self.fields['image'].widget.attrs.update({'class': 'form-control'})

    def clean_name(self):
        name = self.cleaned_data['name']
        name_lower = name.lower()
        for word in FORBIDDEN_WORDS:
            if word in name_lower:
                raise ValidationError(f'Название не должно содержать слово "{word}"')
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        if description:
            desc_lower = description.lower()
            for word in FORBIDDEN_WORDS:
                if word in desc_lower:
                    raise ValidationError(f'Описание не должно содержать слово "{word}"')
        return description

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной')
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Проверка размера
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Размер файла не должен превышать 5 МБ')
            # Проверка формата
            allowed_formats = ['image/jpeg', 'image/png']
            if image.content_type not in allowed_formats:
                raise ValidationError('Допустимые форматы: JPEG, PNG')
        return image
