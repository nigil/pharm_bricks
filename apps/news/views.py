from django.views.generic.base import TemplateView
from news.models import NewsPost
from static_page.models import StaticPage
from django.shortcuts import get_object_or_404


class NewsPageView(TemplateView):
    template_name = 'news/news_page.html'

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        kwargs['page'] = get_object_or_404(StaticPage, slug='news')
        kwargs['news'] = NewsPost.objects.live().order_by('-first_published_at')

        return kwargs