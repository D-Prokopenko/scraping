from django.contrib.auth import authenticate, login, logout, get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.
from django.views import View
import datetime as dt
from scraping.models import Error
from .forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, ContactForm

User = get_user_model()


class LoginView(View):

    """ Авторизация """
    def post(self, request):
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            data = form.cleaned_data
            email = data.get('email')
            password = data.get('password')
            user = authenticate(request, email=email, password=password)
            login(request, user)
            return redirect('home')
        return render(request, 'accounts/login.html', {
            'form': form,
        })

    def get(self, request):
        form = UserLoginForm()
        return render(request, 'accounts/login.html', {
            'form': form,
        })


class LogoutView(View):
    """ Обработка выхода """
    def get(self, request):
        logout(request)
        return redirect('home')


class RegisterView(View):
    """ Регистрация новых пользователей """
    def post(self, request):
        form = UserRegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            messages.success(request, 'Пользователь зарегистрирован.')
            return render(request, 'accounts/register_done.html', {'new_user': new_user, })
        return render(request, 'accounts/register.html', {
            'form': form,
        })

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {
            'form': form,
        })


class PersonAreaView(View):
    """ Личный кабинет """
    def get(self, request):
        if request.user.is_authenticated:
            contact_form = ContactForm()
            user = request.user
            form = UserUpdateForm(initial={'city': user.city, 'language': user.language, 'send_email': user.send_email})
            return render(request, 'accounts/update.html', {
                'form': form,
                'contact_form': contact_form})
        else:
            return redirect('accounts:login')

    def post(self, request):
        user = request.user
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user.city = data['city']
            user.language = data['language']
            user.send_email = data['send_email']
            user.save()
            messages.success(request, 'Данные сохранены.')
            return redirect('accounts:update')
        form = UserUpdateForm(initial={'city': user.city, 'language': user.language, 'send_email': user.send_email})
        return render(request, 'accounts/update.html', {'form': form, })


class DelPersonView(View):
    """ Удаление аккаунта """
    def post(self, request):
        user = request.user
        qs = User.objects.get(pk=user.pk)
        qs.delete()
        messages.error(request, 'Пользователь удален.')
        return redirect('home')


class MsgAdminView(View):
    """ Запрос на добавление города/языка """
    def post(self, request):
        contact_form = ContactForm(request.POST or None)
        if contact_form.is_valid():
            data = contact_form.cleaned_data
            city = data.get('city')
            language = data.get('language')
            email = data.get('email')
            qs = Error.objects.filter(timestamp=dt.date.today())
            if qs.exists():
                err = qs.first()
                data = err.data.get('user_data', [])
                data.append({'city': city, 'email': email, 'language': language})
                err.data['user_data'] = data
                err.save()
            else:
                data = [{'city': city, 'email': email, 'language': language}]
                Error(data=f"user_data: {data}").save()
            messages.success(request, 'Данные отправлены администрации.')
            return redirect('accounts:update')
        else:
            return redirect('accounts:update')

    def get(self, request):
        contact_form = ContactForm()
        return redirect('accounts:login')
