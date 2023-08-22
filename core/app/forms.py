from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import CustomUser


class CustomUserAuthenticationForm(AuthenticationForm):
    pass


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Почта", widget=forms.EmailInput(attrs={
        "class": "modal__form-input",
        "placeholder": "Your email",
        "name": "user-email",
        "autocomplete": "email"
    }))
    phone_number = forms.CharField(label="Номер телефона", widget=forms.NumberInput(attrs={
        "class": "modal__form-input",
        "placeholder": "Your phone number",
        "name": "user-phone",
    }))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={
        "class": "modal__form-input modal__form-password",
        "placeholder": "password",
        "name": "user-password",
    }))
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput(attrs={
        "class": "modal__form-input modal__form-password-rep",
        "placeholder": "Repeat password",
        "name": "user-password-repeat",
    }))

    class Meta:
        model = CustomUser
        fields = ("email", "phone_number", "password1", "password2")
