from django.contrib.auth.models import User
from django import forms
from .models import Song


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


# class SongForm(forms.ModelForm):
#     user = forms.ModelChoiceField(widget=forms.TextInput(attrs={'readonly': 'readonly'}))
#
#     class Meta:
#         model = Song
#         fields = '__all__'
