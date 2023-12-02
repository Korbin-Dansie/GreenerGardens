from django import forms
from .models import Garden, Garden_Section, Plant, Plant_Log, Plant_Category, Plant_Note

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
            'variety': forms.TextInput(attrs={'class': 'form-control'}),
            # 'image': forms.FileInput(attrs={'class':"form-control", "type":"file"}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':5}),
            'seed': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':9223372036854775807}),
            'user': forms.HiddenInput(),
        }

class Plant_CategoryForm(forms.ModelForm):
    class Meta:
        model = Plant_Category
        fields = "__all__"
        widgets =   { 
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'user': forms.HiddenInput(),
        }

class Plant_LogForm(forms.ModelForm):
    class Meta:
        model = Plant_Log
        fields = "__all__"
        widgets =   { 
            'garden_section': forms.HiddenInput(),
            'plant': forms.Select(attrs={'class': 'form-select'}),
            # 'date': forms.DateInput(attrs={'class': 'form-select'})
            'count': forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':9223372036854775807}),
        }

class Plant_NoteForm(forms.ModelForm):
    class Meta:
        model = Plant_Note
        fields = "__all__"
        widgets =   { 
            'plant': forms.HiddenInput(),
            # 'date': forms.DateInput(attrs={'class': 'form-select'})
            'text': forms.Textarea(attrs={'class': 'form-control', 'row':10}),
        }

class Garden_Section_Date_Form(forms.Form):
    year = forms.IntegerField(
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min':0, 'max':9999})
    )
