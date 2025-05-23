from django import forms
from .models import Product
from django.core.exceptions import ValidationError


# Список запрещенных слов
FORBIDDEN_WORDS = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше имя',
            'required': True,
        })
    )
    phone = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Контактный телефон',
            'required': True,
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Введите текст',
            'rows': 4,
            'required': True,
        })
    )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  # все поля модели

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Стилизуем поля формы
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                # Для чекбокса добавим класс
                field.widget.attrs.update({'class': 'form-check-input'})
            else:
                field.widget.attrs.update({'class': 'form-control'})

    def clean_name(self):
        name = self.cleaned_data['name']
        # Проверка на запрещенные слова (регистронезависимо)
        lower_name = name.lower()
        for word in FORBIDDEN_WORDS:
            if word in lower_name:
                raise ValidationError(f"Название не должно содержать слово '{word}'.")
        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        lower_desc = description.lower()
        for word in FORBIDDEN_WORDS:
            if word in lower_desc:
                raise ValidationError(f"Описание не должно содержать слово '{word}'.")
        return description

    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 0:
            raise ValidationError("Цена не может быть отрицательной.")
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Проверка формата файла
            valid_formats = ['image/jpeg', 'image/png']
            if not hasattr(image, 'content_type'):
                raise ValidationError("Некорректный файл изображения.")
            if image.content_type not in valid_formats:
                raise ValidationError("Недопустимый формат. Допустимые форматы изображений: JPEG и PNG.")
            # Проверка размера файла (не более 5 МБ)
            max_size = 5 * 1024 * 1024  # 5 МБ
            if hasattr(image, 'size') and image.size > max_size:
                raise ValidationError("Размер файла не должен превышать 5 МБ.")
        return image
