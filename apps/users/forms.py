from django import forms
from wagtail.wagtailusers.forms import UserEditForm
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.password_validation import validate_password
from cities_light.models import Country, City
from django.core.urlresolvers import reverse_lazy
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordResetForm, UsernameField, SetPasswordForm
)

from core.validators import NameValidator, PhoneValidator
from core.mailer import HTMLTemplateMailer
from django.conf import settings


USER_FORM_FIELDS = {'email', 'first_name', 'phone', 'last_name', 'postcode',
                  'delivery_address', 'country', 'organization', 'city', 'subscribed_on_news'}


class LoginForm(AuthenticationForm):
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True,
                                      'class': 'color_p',
                                      'placeholder': "Email*"}),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'color_p',
                                          'placeholder': "Password*"}),
    )

    error_messages = {
        'invalid_login': _(
            'Your password or login has not been recognised. '
            'Note that both fields are case-sensitive.'
        ),
    }


class CustomPasswordResetForm(PasswordResetForm):
    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            get_user_model().objects.get(email=email)
            return email
        except ObjectDoesNotExist:
            raise forms.ValidationError(_('User with this email does not exists'))

    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        user = context['user']
        mail_subject = 'Password recovery on {}'.format(settings.HOSTNAME)
        HTMLTemplateMailer(user.email, mail_subject, email_template_name, context).send()

    def save(self, **kwargs):
        super(CustomPasswordResetForm, self).save(**kwargs)


class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(strip=False, widget=forms.PasswordInput(
        attrs={'placeholder': 'New password'}))
    new_password2 = forms.CharField(strip=False, widget=forms.PasswordInput(
        attrs={'placeholder': 'New password confirmation'}))


class CustomUserEditForm(UserEditForm):
    last_name = forms.CharField(label=_('Last Name'))
    organization = forms.CharField()
    phone = forms.Field

    country = forms.ModelChoiceField(Country.objects.all().order_by('name'),
                                     empty_label='Country*',
                                     widget=forms.Select(
                                         attrs={'data-load_cities_url': reverse_lazy(
                                                'load_cities_ajax')}))
    city = forms.ModelChoiceField(City.objects.none(), empty_label='City*')

    delivery_address = forms.CharField()
    postcode = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(CustomUserEditForm, self).__init__(*args, **kwargs)

        if self.data.get('country'):
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by(
                    'name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk and self.instance.country:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')


class CustomUserCreationForm(CustomUserEditForm):
    pass


class UserForm(forms.ModelForm):
    first_name = forms.CharField(
        validators=[NameValidator()],
        widget=forms.TextInput(attrs={'placeholder': 'First Name*'}))
    last_name = forms.CharField(
        validators=[NameValidator()],
        widget=forms.TextInput(attrs={'placeholder': 'Last Name*'})
    )
    phone = forms.CharField(
        validators=[PhoneValidator()],
        widget=forms.TextInput(attrs={'placeholder': 'Telephone number*'})
    )
    organization = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Company*'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email*'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password*'}))
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Password confirmation*'}))
    country = forms.ModelChoiceField(Country.objects.all().order_by('name'), empty_label='Country*',
                                     widget=forms.Select(
                                         attrs={'class': 'show_check_bask text-left sity',
                                                'data-load_cities_url': reverse_lazy(
                                                    'load_cities_ajax')}))
    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={'placeholder': 'Delivery address*',
                                     'class': 'adres', 'cols': 27, 'rows': 3}))
    city = forms.ModelChoiceField(City.objects.none(), empty_label='City*',
                                  widget=forms.Select(
                                      attrs={'class': 'show_check_bask text-left sity'}))
    postcode = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Postcode*'}))
    subscribed_on_news = forms.BooleanField(required=False,
                                            widget=forms.CheckboxInput(attrs={'class': 'checkbox'}))

    def clean_city(self):
        city = self.cleaned_data.get('city')
        if not city:
            raise forms.ValidationError(_('Choose the city'))
        return city

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            get_user_model().objects.get(email=email)
            raise forms.ValidationError(_('This email address already exists.'))
        except ObjectDoesNotExist as e:
            return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        validate_password(self.cleaned_data.get('password'))
        return password

    def clean_password1(self):
        password = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        if (password or password1) and password != password1:
            raise forms.ValidationError(_('The password does not match.'))
        return password1

    class Meta:
        model = get_user_model()
        fields = USER_FORM_FIELDS
        abstract = True

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        if self.data.get('country'):
            try:
                country_id = int(self.data.get('country'))
                self.fields['city'].queryset = City.objects.filter(country_id=country_id).order_by(
                    'name')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk and self.instance.country:
            self.fields['city'].queryset = self.instance.country.city_set.order_by('name')


class RegisterForm(UserForm):
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = True
        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = USER_FORM_FIELDS | {'password'}


class ProfileForm(UserForm):
    password = forms.CharField(required=False,
                               help_text='Leave blank if not changing',
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'Password'}))
    password1 = forms.CharField(required=False,
                                help_text='Enter the same password as above, for verification',
                                widget=forms.PasswordInput(
                                    attrs={'placeholder': 'Password confirmation'}))

    def clean_email(self):
        return self.cleaned_data.get('email')

    def save(self, commit=True):
        user = super(ProfileForm, self).save(commit=False)
        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user

    class Meta:
        model = get_user_model()
        fields = USER_FORM_FIELDS
