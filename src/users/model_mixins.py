from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


User = get_user_model()


class DateMixin(models.Model):
    '''Даты создания и редактирования'''
    created_at = models.DateTimeField(verbose_name='create_at', null=True, blank=False)
    updated_at = models.DateTimeField(verbose_name='updated_at', null=True, blank=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk and not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        return super(DateMixin, self).save(*args, **kwargs)


class InfoMixin(DateMixin):
    '''Пользователь создавший и редактировавший'''
    created_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name='created_%(app_label)s_%(class)s', # делаем различие в related_name в зависимости от
                                                        # названия приложения app_label и названия класса
                                                        # class где используем миксин
        verbose_name='Created by',
        null=True,)
    updated_by = models.ForeignKey(
        to=User,
        on_delete=models.SET_NULL,
        related_name='updated_%(app_label)s_%(class)s',
        verbose_name='Updated by',
        null=True,)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        from crum import get_current_user # позволяет получить пользователя из запроса

        user = get_current_user() # получаем пользователя из  запроса
        if user and not user.pk:
            user = None
        if not self.pk:
            self.created_by = user
        self.updated_by = user
        super().save(*args, **kwargs)

