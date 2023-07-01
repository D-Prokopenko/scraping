from django.db import models
import jsonfield
from .utils import from_cyrillic_to_lat


# Create your models here.

def default_urls():
    return {'rabota': '',
            'superjob': ''}

class City(models.Model):
    """ Модель городов """
    name = models.CharField(max_length=50,
                            verbose_name="Название населенного пункта",
                            unique=True)
    slug = models.CharField(max_length=50, blank=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_lat(str(self.name))

        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = "Название населенного пункта"
        verbose_name_plural = "Название населенных пунктов"


class Language(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name="Язык программирования",
                            unique=True)
    slug = models.CharField(max_length=50,
                            blank=True,
                            unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = from_cyrillic_to_lat(str(self.name))

        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name ='Язык программирования'
        verbose_name_plural = "Язаки програмиирования"


class Vacancy(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название вакансии")
    company = models.CharField(max_length=200, verbose_name='Компания')
    description = models.TextField(verbose_name='Описание вакансии')
    url = models.URLField(unique=True)
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name="Город")
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name="Язык программирования")
    timestamp = models.DateField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.title} - {self.company}'

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ['-timestamp']


class Error(models.Model):
    timestamp = models.DateField(auto_now_add=True, blank=True)
    data = jsonfield.JSONField()

    def __str__(self):
        return f'{self.timestamp}'
    
    class Meta:
        verbose_name = 'Ошибку'
        verbose_name_plural = 'Ошибки'


class Url(models.Model):
    city = models.ForeignKey('City', on_delete=models.CASCADE, verbose_name="Город")
    language = models.ForeignKey('Language', on_delete=models.CASCADE, verbose_name="Язык программирования")
    url_data = jsonfield.JSONField(default=default_urls)

    class Meta:
        unique_together = ("city", "language")
