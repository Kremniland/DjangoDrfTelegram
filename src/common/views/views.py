from django.shortcuts import render
from django.views import generic
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import render, HttpResponseRedirect

from src.common.forms.users_forms import UserLoginForm, UserRegistrationForm, UserUpdateForm
from src.common.models import EmailVerification

User = get_user_model()


class TitleMixin:
    title = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['title'] = self.title
        return context


class UserRegistrationView(TitleMixin, generic.CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('common:login')
    title = 'Регистрация'


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Авторизация'


class UserUpdateView(TitleMixin, generic.UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/profile.html'
    title = 'Личный кабинет'

    def get_success_url(self):
        return reverse_lazy('common:profile')

    def get_object(self, queryset=None):
        return self.request.user


class EmailVerificationView(TitleMixin, TemplateView):
    template_name = 'users/email_verification.html'
    title = 'Верификация почты'

    def get(self, request, *args, **kwargs):
        '''берем данные из гет запроса при переходе юзера по ссылке,
        проверяем время жизни ссылки и верифицируем'''
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        # берем filter для того если нет такого пользователя не выскочит ошибки
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        # если список не пустой и время жизни ссылки не истекло то верифицируем юзера
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified = True
            user.save()
            # обязательно вернуть так или не отработает шаблон
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            # если проверка не прошла перекинем на логин страницу
            return HttpResponseRedirect(reverse('common:login'))


