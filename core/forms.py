# forms.py
from django import forms
from .models import ConnectedClient

class ClienteForm(forms.ModelForm):
    class Meta:
        model = ConnectedClient
        fields = ['nome']
