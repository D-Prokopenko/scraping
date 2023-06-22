from django.shortcuts import render
from django.views.generic.base import View
from .models import Vacancy
# Create your views here.


class HomeView(View):
    """ Домашняя страница """
    def get(self, request):
        vacancy = Vacancy.objects.all()
        return render(request, 'scraping/home.html', {
            'vacancy': vacancy,
            })