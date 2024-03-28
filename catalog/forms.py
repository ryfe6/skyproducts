from django import forms

from catalog.models import Product, Version


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

    def clean(self):
        cleaned_data = self.cleaned_data['name']
        cleaned_description = self.cleaned_data['description']
        list_including = ('казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция',
                          'радар')

        for word in list_including:
            if word in cleaned_data or word in cleaned_description:
                raise forms.ValidationError(f'Запрещено использование слова - "{word}"')

        return cleaned_data, cleaned_description


class VersionForm(forms.ModelForm):
    model = Version
    fields = '__all__'

    class Meta:
        model = Version
        fields = '__all__'
