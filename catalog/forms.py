from django import forms

from catalog.models import Product, Category, ForbiddenWords, ProductVersion, Contact


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

class ProductForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Product
        fields = ('name', 'description', 'photo', 'category', 'price')

    def clean_name(self):

        cleaned_data = self.cleaned_data['name']
        if any(obj.word.lower() in cleaned_data.lower() for obj in ForbiddenWords.objects.all()):
            raise forms.ValidationError('Этот продукт запрещён')
        return cleaned_data

    def clean_description(self):
        cleaned_data = self.cleaned_data['description']
        if any(obj.word.lower() in cleaned_data.lower() for obj in ForbiddenWords.objects.all()):
            raise forms.ValidationError('Этот продукт запрещён')
        return cleaned_data


class ProductVersionForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = ProductVersion
        fields = ('num', 'name', 'is_actual')

    def clean_is_actual(self):
        cleaned_data = self.cleaned_data['is_actual']
        #if cleaned_data:
        return cleaned_data


class ContactForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('name', 'phone_number', 'user_text')
