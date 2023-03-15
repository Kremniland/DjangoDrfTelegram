from django.db import models


class UserTg(models.Model):
    user_tg_id = models.IntegerField(unique=True, verbose_name='Телеграм ID')
    first_name = models.CharField(max_length=256, blank=True, null=True, verbose_name='Имя')
    username = models.CharField(max_length=256, blank=True, null=True, verbose_name='Ник')
    create_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user_tg_id} - {self.first_name} - {self.username}'

    class Meta:
        db_table = 'user_tg'
        verbose_name = 'Пользователь телеграмм'
        verbose_name_plural = 'Пользователи телеграмм'


class Message(models.Model):
    text = models.TextField(verbose_name='Текст сообщения')
    chat_id = models.IntegerField(verbose_name='Чат ID')
    create_date = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(
        to=UserTg,
        on_delete=models.RESTRICT,
        related_name='message',
        verbose_name='Пользователь'
    )

    class Meta:
        db_table = 'message'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

