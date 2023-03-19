import uuid
from datetime import timedelta
from django.utils.timezone import now
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from django.contrib.auth import get_user_model

from src.common.models import EmailVerification

User = get_user_model()


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'
    }))
    class Meta:
        model = User
        fields = ('username', 'password',)


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите фамилию'}))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите адрес эл. почты'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control py-4', 'placeholder': 'Подтвердите пароль'}))

    def save(self, commit=True):
        '''Создается объект EmailVerification при создании нового пользователя
            и отправляем на него ссылку подтверждения'''
        # получаем объект пользователя из заполненной формы и сохраняем его
        user = super(UserRegistrationForm, self).save(commit=True)
        # время жизни ссылки
        expiration = now() + timedelta(hours=48)
        # формируем и записываем объект EmailVerification
        record = EmailVerification.objects.create(
            code=uuid.uuid4(),
            user=user,
            expiration=expiration
        )
        # Вызываем метод прописанный в модели для отправки email
        record.send_verification_mail()
        return user # возвращаем пользователя

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class UserUpdateForm(UserChangeForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}), required=False)
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}), required=False)
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'image', 'username', 'email']
