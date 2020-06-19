from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from authenticator.models import FrontAuth, AuthLogs ,Users
from django.utils.translation import gettext as _
# Register your models here.


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['uname','email','name']
    fieldsets= (
        (None, {'fields': ('uname','password')}),
        (_('Profile Info'), {'fields': ('email','name')}),
        (_('Permissions'), {'fields': ('is_omega','is_alpha','is_beta','is_staff','is_superuser')}),
        (_('Important Dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets= (
        (None, {'classes': ('wide',),'fields': ('name','password1','password2')}),
    )


admin.site.register(Users, UserAdmin)
admin.site.register(FrontAuth)
admin.site.register(AuthLogs)
