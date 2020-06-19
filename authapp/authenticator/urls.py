from django.conf.urls import url
from django.urls import path
from authenticator import views
from django.conf.urls import include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', views.UsersViewSet)


app_name = 'authenticator'

urlpatterns = [
    url(r'^addUser/$',views.addUser, name="addUser"),
    url(r'^login/$',views.loginAuth, name="login"),
    path('CreateUser/', views.CreateUserView.as_view(), name="create_user"),
    path('authUser/', views.CreateTokenView.as_view(), name="create_token"),
    path('manageUser/', views.ManageUsersView.as_view(), name="manage_user"),
    path('', include(router.urls)),
]