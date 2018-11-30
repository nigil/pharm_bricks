import os
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from static_page.models import StaticPage, HomeSlider
from django.shortcuts import get_object_or_404
from static_page.forms import QuestionForm
from django.core.urlresolvers import reverse_lazy
from core.models import PharmBricksSettings
from core.mailer import HTMLTemplateMailer
from django.conf import settings
from django.contrib import messages
from screening_libraries.services import delete_old_reaction_files


class HomePage(TemplateView):
    template_name = 'pages/home_page.html'

    def get_context_data(self, **kwargs):
        # this page will be visit most often, so put this code here
        if self.request.user.is_authenticated:
            result_files_dir = os.path.join(settings.TEMP_FILES_DIR, str(self.request.user.id))
            if os.path.exists(result_files_dir):
                delete_old_reaction_files(result_files_dir)

        if 'view' not in kwargs:
            kwargs['view'] = self

        home_page = get_object_or_404(StaticPage, slug='home')
        kwargs['page'] = home_page

        kwargs['home_sliders'] = HomeSlider.objects.live()

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
        mail_subject = 'Feedback form question'
        site_settings = PharmBricksSettings.for_site(self.request.site)
        mailer = HTMLTemplateMailer(site_settings.admin_email,
                                    mail_subject,
                                    'email/contacts_question.html',
                                    {
                                        'form_data': form.cleaned_data,
                                        'site_host': settings.HOSTNAME
                                    })
        mailer.send()

        messages.add_message(self.request, messages.INFO,
                             'Thank you for your question! '
                             'We will respond within 24 hours.')

        return super(ContactsPage, self).form_valid(form)

