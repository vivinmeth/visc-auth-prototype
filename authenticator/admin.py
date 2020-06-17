from django.contrib import admin
from authenticator.models import FrontAuth, AuthLogs ,Users
# Register your models here.

admin.site.register(Users)
admin.site.register(FrontAuth)
admin.site.register(AuthLogs)
