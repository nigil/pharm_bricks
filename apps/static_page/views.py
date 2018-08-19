from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from static_page.models import StaticPage
from django.shortcuts import get_object_or_404
from static_page.forms import QuestionForm
from django.core.urlresolvers import reverse_lazy
from core.mailer import HTMLTemplateMailer
from django.conf import settings
from django.contrib import messages


class HomePage(TemplateView):
    template_name = 'pages/home_page.html'

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        kwargs['page'] = get_object_or_404(StaticPage, slug='home')

        return kwargs


class ContactsPage(FormView):
    template_name = 'pages/contacts_page.html'
    form_class = QuestionForm
    success_url = reverse_lazy('contacts')

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        kwargs['page'] = get_object_or_404(StaticPage, slug='contacts')

        return kwargs

    def form_valid(self, form):
        mail_subject = 'Your have asked a question from Pharm Bricks'
        mailer = HTMLTemplateMailer(settings.ADMIN_EMAIL,
                                    mail_subject,
                                    'email/contacts_question.html',
                                    {
                                        'form_data': form.cleaned_data,
                                        'site_host': settings.HOSTNAME
                                    })
        mailer.send()

        messages.add_message(self.request, messages.INFO,
                             'You question was successfully send. Our managers will contact you soon.')

        # return(HttpResponseRedirect(reverse_lazy('home')))

        return super(ContactsPage, self).form_valid(form)

