from django import forms
from .models import Garden

class GardenForm(forms.ModelForm):
    class Meta:
        model = Garden
        fields = "__all__"
        widgets =   { 
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.HiddenInput(),
        }