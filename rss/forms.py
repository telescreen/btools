from django import forms
from django.core.validators import URLValidator
from .models import Category, Source


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
    name = forms.CharField(label="Category Name", max_length=200, required=True)
    description = forms.CharField(label="Category Description", widget=forms.Textarea, max_length=1000)


class SourceForm(forms.ModelForm):
    class Meta:
        model = Source
        fields = ['url', 'category']
    url = forms.CharField(label="Source URL", max_length=200, required=True,
                          validators=[URLValidator()])