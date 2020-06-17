from django.conf.urls import url
from authenticator import views

app_name = 'authenticator'

urlpatterns = [
    url(r'^addUser/$',views.addUser, name="addUser"),
    url(r'^login/$',views.loginAuth, name="login"),

]