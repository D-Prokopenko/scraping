from django.contrib import admin
from .models import City, Language, Vacancy, Error, Url

# Register your models here.

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    """ Отображение городов """
    list_display = ('name', 'slug', )


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    """ Отображение языков программирования """
    list_display = ('name', 'slug', )


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    """ Отображение вакансий """
    list_display = ('title', 'company', )


@admin.register(Error)
class ErrorAdmin(admin.ModelAdmin):
    """ Отображение ошибок """
    list_display = ('timestamp', )

@admin.register(Url)
class ErrorAdmin(admin.ModelAdmin):
    """ Отображение ошибок """
    list_display = ("city", "language")