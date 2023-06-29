from django.core.paginator import Paginator
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


class ListView(View):
    """ Страница с вакансиями """
    def get(self, request):
        city = request.GET.get('city')
        language = request.GET.get('language')
        context = {'city': city, 'language': language}
        if city or language:
            _filter = {}
            if city:
                _filter['city__slug'] = city
            if language:
                _filter['language__slug'] = language
            vacancy = Vacancy.objects.filter(** _filter)
            paginator = Paginator(vacancy, 10)  # Show 10 contacts per page.

            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)
            context['vacancy'] = page_obj
        return render(request, 'scraping/list.html', context)
