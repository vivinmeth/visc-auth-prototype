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
    path('get_login_token/', views.CSRFToken.as_view(), name="csrf_middleware"),
    path('get_login_status/', views.CheckTokenView.as_view(), name="check_auth"),
    path('', include(router.urls)),
]