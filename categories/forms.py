from django import forms
from django.core.exceptions import ValidationError
from .models import Category


class CategoryForm(forms.ModelForm):
    """Kategoriya yaratish va tahrirlash"""

    class Meta:
        model = Category
        fields = ['name', 'type']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Kategoriya nomi',
                'required': True
            }),
            'type': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            })
        }
        labels = {
            'name': 'Nomi',
            'type': 'Turi'
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')

        if not name or len(name) < 2:
            raise ValidationError('Kategoriya nomi kamida 2 ta belgidan iborat bo\'lishi kerak')

        return name