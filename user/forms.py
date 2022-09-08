from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.forms import TextInput, FileInput, Textarea

from place.models import Place, PlaceLanguage
from user.models import UserProfile


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, label='User Name:')
    email = forms.CharField(max_length=100, label='Email:')
    first_name = forms.CharField(max_length=100, help_text='First Name', label='First Name:')
    last_name = forms.CharField(max_length=100, help_text='Last Name', label='Last Name:')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': TextInput(attrs={'class': 'input', 'placeholder': 'username'}),
            'email': TextInput(attrs={'class': 'input', 'placeholder': 'Email'}),
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}),
            'password1': TextInput(attrs={'class': 'input', 'placeholder': 'password1'}),
            'password2': TextInput(attrs={'class': 'input', 'placeholder': 'password2'}),
        }

class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets={
            'username':TextInput( attrs={'class':'input','placeholder':'username'}),
            'email': TextInput(attrs={'class': 'input', 'placeholder': 'Email'}),
            'first_name': TextInput(attrs={'class': 'input', 'placeholder': 'First Name'}),
            'last_name': TextInput(attrs={'class': 'input', 'placeholder': 'Last Name'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model=UserProfile()
        fields = ['phone', 'address', 'city', 'country','lang', 'image']
        widgets = {
            'phone': TextInput(attrs={'class': 'input', 'placeholder': 'Phone'}),
            'address': TextInput(attrs={'class': 'input', 'placeholder': 'Address'}),
            'city': TextInput(attrs={'class': 'input', 'placeholder': 'City'}),
            'country': TextInput(attrs={'class': 'input', 'placeholder': 'Country'}),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'Image Profile'}),
        }
class PlaceUpdateForm(forms.ModelForm):
    class Meta:
        model=Place()
        fields = ['category', 'title', 'keyword', 'description', 'city', 'country', 'location', 'image', 'detail',
                  'status', ]
        widgets = {
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'Title'}),
            'keyword': TextInput(attrs={'class': 'input', 'placeholder': 'keyword'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'Your description'}),
            'city': TextInput(attrs={'class': 'input', 'placeholder': 'City'}),
            'location': TextInput(attrs={'class': 'input', 'placeholder': 'location'}),
            'country': TextInput(attrs={'class': 'input', 'placeholder': 'Country'}),
        }
class PlaceLangUpdateForm(forms.ModelForm):
    class Meta:
        model=PlaceLanguage()
        fields = ['lang','title', 'keyword', 'description', 'detail',]
        widgets = {
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'Title'}),
            'keyword': TextInput(attrs={'class': 'input', 'placeholder': 'keyword'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'Your description'}),
            'detail': Textarea(attrs={'class': 'input', 'placeholder': 'detail'}),
        }