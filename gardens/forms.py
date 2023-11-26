from django import forms
from .models import Garden, Garden_Section, Plant

class GardenForm(forms.ModelForm):
    class Meta:
        model = Garden
        fields = "__all__"
        widgets =   { 
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'image': forms.FileInput(attrs={'class':"form-control", "type":"file"}),
            'image_alt': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.HiddenInput(),
        }

class Garden_SectionForm(forms.ModelForm):
    class Meta:
        model = Garden_Section
        fields = "__all__"
        widgets =   { 
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'garden': forms.HiddenInput(),
        }


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = "__all__"
        widgets =   { 
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            # 'image': forms.FileInput(attrs={'class':"form-control", "type":"file"}),
            'category': forms.TextInput(attrs={'class': 'form-select'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':5}),
            'seed': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':9223372036854775807}),
            'user': forms.HiddenInput(),
        }