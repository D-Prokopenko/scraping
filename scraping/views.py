from django.shortcuts import render
from django.views.generic.base import View

from .forms import FindForm
from .models import Vacancy
# Create your views here.


class HomeView(View):
    """ Домашняя страница """
    def get(self, request):
        form = FindForm()
        return render(request, 'scraping/home.html', {
            'form': form,
        })


class SearchView(View):
    """ Страница с вакансиями """
    def get(self, request):
        vacancy = []
        city = request.GET.get('city')
        language = request.GET.get('language')
        if city or language:
            _filter = {}
            if city:
                _filter['city__slug'] = city
            if language:
                _filter['language__slug'] = language
            vacancy = Vacancy.objects.filter(** _filter)
        return render(request, 'scraping/search.html', {
            'vacancy': vacancy,
            })
