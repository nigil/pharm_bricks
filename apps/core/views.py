from django.shortcuts import render
from django.template.loader import render_to_string
from cities_light.models import Country, City
from django.http import HttpResponseBadRequest, HttpResponse


def homepage(request):
    return render(request, 'base.html')


def load_cities_ajax(request):
    if not request.is_ajax():
        return HttpResponseBadRequest()
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    html = render_to_string('utilites/city_dropdown_list_options.html', {'cities': cities})
    return HttpResponse(html)
