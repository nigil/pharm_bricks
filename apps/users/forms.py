from django import forms
from wagtail.wagtailusers.forms import UserEditForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.password_validation import validate_password


class CustomUserEditForm(UserEditForm):
    last_name = forms.CharField(required=False, label=_('Last Name'))
    organization = forms.CharField()
    phone = forms.Field

    country = forms.CharField(required=False)
    region = forms.CharField(required=False)
    city = forms.CharField(required=False)

    delivery_address = forms.CharField()
    postcode = forms.CharField(required=False)


class CustomUserCreationForm(UserCreationForm):
    last_name = forms.CharField(required=False, label=_('Last Name'))
    organization = forms.CharField()
    phone = forms.CharField()

    country = forms.CharField(required=False)
    region = forms.CharField(required=False)
    city = forms.CharField(required=False)

    delivery_address = forms.CharField()
    postcode = forms.CharField(required=False)


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    password1 = forms.CharField(widget=forms.PasswordInput(), label='Repeat password')

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(self.cleaned_data.get('password'))
        return password

    def clean_password1(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if password and password1 and password != password1:
            raise forms.ValidationError(_('Retype Password must be repeated exactly.'))
        return password1

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = ('email', 'password', 'password1', 'first_name', 'last_name', 'organization', 'region')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['region'].required = False
        self.fields['last_name'].required = False
