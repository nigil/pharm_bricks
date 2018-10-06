from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView,
    PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
)
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView, UpdateView
from users.forms import (
    RegisterForm, LoginForm, CustomPasswordResetForm, CustomSetPasswordForm, ProfileForm
)
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect
from core.mailer import HTMLTemplateMailer
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from users.tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponseForbidden, JsonResponse
from shop.models import Order
from bookmarks.models import ProductBookmark, GeneratorResultBookmark

user_model = get_user_model()


class PbLogin(LoginView):
    template_name = 'registration/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True
    redirect_field_name = 'next'


class PbLogout(LogoutView):
    next_page = reverse_lazy('home')


class PbRegister(FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('register')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('home')
        return super(PbRegister, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()

        mail_subject = 'Registering on {}'.format(settings.HOSTNAME)
        # request_meta = self.request.META
        # site_host = request_meta.get('HTTP_ORIGIN') if request_meta.get('HTTP_ORIGIN') \
        #     else request_meta.get('HTTP_HOST')
        confirm_link = self.request.build_absolute_uri(reverse('confirm_email', args=(
            urlsafe_base64_encode(force_bytes(user.id)),
            account_activation_token.make_token(user)))
        )
        login_link = self.request.build_absolute_uri(reverse('login'))
        reset_password_link = self.request.build_absolute_uri(reverse('password_reset'))
        HTMLTemplateMailer(user.email, mail_subject, 'email/confirm_email.html',
                           {
                               'confirm_link': confirm_link,
                               'login_link': login_link,
                               'reset_password_link': reset_password_link,
                               'info_email': settings.INFO_EMAIL,
                               'user_data': form.cleaned_data,
                               'site_host': settings.HOSTNAME

                           }).send()

        messages.add_message(self.request, messages.INFO,
                             'You have just registered on our site. '
                             'Please check your email for next instructions')

        return super(PbRegister, self).form_valid(form)


def confirm_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = user_model.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user_model.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.INFO, 'Thank you for your email confirmation. '
                                                     'Now you can <a href="'
                                                     + reverse('login')
                                                     + '">login</a> your account.')
    else:
        messages.add_message(request, messages.INFO, 'Activation link is invalid!')

    return render(request, 'registration/register.html')


class PbPasswordReset(PasswordResetView):
    token_generator = account_activation_token
    template_name = 'registration/password_reset.html'
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('password_reset')
    html_email_template_name = 'registration/password_reset_html_email.html'
    email_template_name = 'registration/password_reset_html_email.html'
    extra_email_context = {'site_host': settings.HOSTNAME}

    def form_valid(self, form):
        messages.add_message(self.request,
                             messages.INFO,
                             '<p>We\'ve emailed you instructions for setting your password, '
                             'if an account exists with the email you entered. '
                             'You should receive them shortly.</p>'
                             '<p>If you don\'t receive an email, please make sure '
                             'you\'ve entered the address you registered with, '
                             'and check your spam folder.</p>')

        return super(PbPasswordReset, self).form_valid(form)


class PbPasswordResetConfirm(PasswordResetConfirmView):
    token_generator = account_activation_token
    success_url = reverse_lazy('password_reset')
    template_name = 'registration/password_reset_set_new.html'
    form_class = CustomSetPasswordForm

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO,
                             '<p>Password was successfully changed.</p>')

        return super(PbPasswordResetConfirm, self).form_valid(form)


class PbPasswordResetComplete(PasswordResetCompleteView):
    pass


class PbPasswordChange(PasswordChangeView):
    pass


class PbPasswordChangeDone(PasswordChangeDoneView):
    pass


class Profile(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.add_message(self.request, messages.INFO,
                             'Profile successfully updated')

        return super(Profile, self).form_valid(form)


class Orders(LoginRequiredMixin, ListView):
    template_name = 'users/orders.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created_date')


class Bookmarks(LoginRequiredMixin, TemplateView):
    template_name = 'users/bookmarks.html'

    def get_context_data(self, **kwargs):
        context = super(Bookmarks, self).get_context_data(**kwargs)

        product_bookmarks = ProductBookmark.objects \
            .select_related('product') \
            .filter(user=self.request.user) \
            .order_by('-created')

        generator_bookmarks = GeneratorResultBookmark.objects \
            .filter(user=self.request.user) \
            .order_by('-created')

        context['product_bookmarks'] = product_bookmarks
        context['generator_bookmarks'] = generator_bookmarks
        context['company_phone'] = settings.COMPANY_PHONE

        return context


class Subscribe(LoginRequiredMixin, TemplateView):
    template_name = 'users/subscribe.html'


def change_news_subscribe(request):
    if not request.is_ajax() or not request.user.is_authenticated:
        return HttpResponseForbidden()

    changed = False

    subscribe_value = request.GET.get('subscribe')
    if subscribe_value == 'true':
        subscribe_value = True
    elif subscribe_value == 'false':
        subscribe_value = False
    else:
        subscribe_value = None

    if isinstance(subscribe_value, bool):
        if subscribe_value != request.user.subscribed_on_news:
            request.user.subscribed_on_news = subscribe_value
            request.user.save()
            changed = True

    return JsonResponse({'changed': changed})
