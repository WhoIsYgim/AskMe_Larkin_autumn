from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Username'}),
                               label="Your Username", max_length=50)
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': '********'}),
                               label="Password", max_length=50)

    def clean_password(self):
        data = self.changed_data['password']
        if len(data) < 8:
            raise ValidationError("Password must contain at least 8 characters.")
        return data

    def clean_username(self):
        data = self.changed_data['username']
        if len(data) < 5:
            raise ValidationError("Username must contain at least 5 characters.")
        return data


