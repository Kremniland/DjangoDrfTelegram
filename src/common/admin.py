from django.contrib import admin

from .models import EmailVerification


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('code', 'user', 'expiration', 'create')
    fields = ('code', 'user', 'expiration', 'create')
    readonly_fields = ('create',)
