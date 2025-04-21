from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('phone',)

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        return password

    def clean_username(self):
        phone = self.cleaned_data.get("phone")
        if len(phone) < 11:
            raise ValidationError("phone must be at least 11 characters")
        return phone

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# class RegisterForm(forms.Form):
#     phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'appearance-none bg-transparent w-full py-3',
#                                                           'placeholder': 'شماره تلفن خود را وارد کنید . . . '}))
#
#
# class CheckOtpForm(forms.Form):
#     code = forms.CharField(widget=forms.TextInput(attrs={'class': 'appearance-none bg-transparent w-full py-3',
#                                                          'placeholder': 'رمز عبور ارسال شده را وارد کنید . . . '}))