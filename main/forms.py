from django import forms
from .models import Main
from django.core.exceptions import ValidationError

class MainForm(forms.ModelForm):
    class Meta:
        model = Main
        fields = "__all__"
        widgets = {
            'font': forms.ClearableFileInput(attrs={'accept': '.ttf'}),
        }
