from django.db import models
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.timezone import now

from django.conf import settings


User = get_user_model()


class EmailVerification(models.Model):
    code = models.UUIDField(unique=True, verbose_name='Код для верификации')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользолватель')
    create = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    expiration = models.DateTimeField(verbose_name='Время жизни ссылки')

    def __str__(self):
        return f'Верификация для {self.user.email}'

    def send_verification_mail(self):
        '''отправка email со ссылкой для подтверждения verification_link'''
        link = reverse('common:verify', kwargs={'email': self.user.email, 'code': self.code})
        verification_link = f'{settings.DOMAIN_NAME}{link}' # формируем полную ссылку Host + ссылка
        subject = 'Подтверждение учетной записи'
        message = 'Для подтверждения {} пройдите по ссылке: {}'.format(
            self.user.email,
            verification_link
        )
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.user.email],
            fail_silently=False,
        )

    def is_expired(self):
        '''проверка срока годности ссылки'''
        return True if now() >= self.expiration else False

    class Meta:
        verbose_name = 'Email верификация'
        verbose_name_plural = 'Email верификация'


class ContactModel(models.Model):
    '''модель для сохранения контакта по емаил'''
    name = models.CharField(max_length=128, blank=True, null=True, verbose_name='Имя')
    subject = models.TextField(max_length=5000, blank=True, null=True, verbose_name='Текст письма')
    email = models.EmailField(max_length=256, verbose_name='Email')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        db_table = "contact_db"
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
        ordering = ('name',)



