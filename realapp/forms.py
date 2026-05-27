from django import forms

from django.contrib.auth.forms import UserCreationForm

from .models import User, Property


# REGISTER FORM
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegisterForm(UserCreationForm):

    class Meta:

        model = User

        fields = [
            'username',
            'email',
            'phone',
            'role',
            'password1',
            'password2'
        ]

        widgets = {

            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter username'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter email'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter phone number'
                }
            ),

            'role': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })

        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

# PROPERTY FORM

class PropertyForm(forms.ModelForm):

    class Meta:

        model = Property

        exclude = ['owner']

        widgets = {

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter property title'
                }
            ),

            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Enter property description'
                }
            ),

            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter property price'
                }
            ),

            'location': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter property location'
                }
            ),

            'property_type': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'bedrooms': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'bathrooms': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                }
            ),

            'area': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter property area'
                }
            ),

            'image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }