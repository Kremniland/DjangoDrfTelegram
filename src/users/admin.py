from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from .models import User, Profile


class ProfileAdmin(admin.StackedInline):
    model = Profile
    fields = ('gender', 'info',)


@admin.register(User)
class UserAdmin(UserAdmin): # Наследуемся от UserAdmin
    change_user_password_template = None
    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'username', 'tg_user_id')}),
        (_('Личная информация'),
         {'fields': ('first_name', 'last_name', 'avatar',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'phone_number', 'password1', 'password2',),
        }),
    )
    list_display = ('id', 'username', 'full_name', 'email', 'phone_number', 'avatar_show',)

    list_display_links = ('id', 'username')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups',)
    search_fields = ('first_name', 'last_name', 'id', 'email', 'phone_number',)
    ordering = ('-id',)
    filter_horizontal = ('groups', 'user_permissions',)
    readonly_fields = ('last_login',)

    inlines = (ProfileAdmin,)

    def avatar_show(self, obj):
        '''Вывод маленькой картинки в админке'''
        if obj.avatar:
            return mark_safe("<img src='{}' width='40' />".format(obj.avatar.url))
        return None



