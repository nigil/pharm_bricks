from django.contrib.auth.views import LoginView, LogoutView, \
    PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView, \
    PasswordChangeView, PasswordChangeDoneView
from django.views.generic import DetailView
from django.views.generic.edit import FormView
from users.forms import RegisterForm
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from core.mailer import HTMLTemplateMailer
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from users.tokens import account_activation_token
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

User = get_user_model()


class PbLogin(LoginView):
    template_name = 'registration/login.html'


class PbLogout(LogoutView):
    pass


class PbRegister(FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('register_success')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super(PbRegister, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()

        current_site = get_current_site(self.request)
        mail_subject = 'Registering on {}'.format(current_site.domain)
        confirm_link = self.request.build_absolute_uri(reverse('confirm_email', args=(
                                                               urlsafe_base64_encode(force_bytes(user.id)),
                                                               account_activation_token.make_token(user))))
        HTMLTemplateMailer(user.email, mail_subject, 'email/confirm_email.html',
                           {'confirm_link': confirm_link}).send()

        return super(PbRegister, self).form_valid(form)


def register_success(request):
    if request.user.is_authenticated():
        return redirect(reverse('home'))
    return render(request, 'registration/register_success.html')


def confirm_email(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


class PbPasswordReset(PasswordResetView):
    token_generator = account_activation_token


class PbPasswordResetConfirm(PasswordResetConfirmView):
    token_generator = account_activation_token


class PbPasswordResetDone(PasswordResetDoneView):
    pass


class PbPasswordResetComplete(PasswordResetCompleteView):
    pass


class PbPasswordChange(PasswordChangeView):
    pass


class PbPasswordChangeDone(PasswordChangeDoneView):
    pass


class Profile(DetailView):
    context_object_name = 'user'
    template_name = 'users/profile.html'

    def get_object(self, queryset=None):
        return self.request.user
