from django import forms
from .models import Main, FieldMenu
from django.core.exceptions import ValidationError

class MainForm(forms.ModelForm):
    class Meta:
        model = Main
        fields = "__all__"
        exclude = ['utama',]
        widgets = {
            'font': forms.ClearableFileInput(attrs={'accept': '.ttf'}),
        }

class FieldMenuForm(forms.ModelForm):
    class Meta:
        model = FieldMenu
        fields = "__all__"
