from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager


# Create your models here.

class UsersManager(BaseUserManager):
    """Users Manager for Django CLI"""

    def create_user(self, uname, email, name, password=None):
        """ New User """
        if not uname or not email:
            raise ValueError("Users must enter Username and Email")

        email= self.normalize_email(email)
        user = self.model(uname=uname, email=email, name=name)
        user.is_superuser = False
        user.is_omega = False
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_omegauser(self, uname, email, name, password):
        """ New Omega User """
        user = self.create_user(uname, email, name, password)

        user.is_superuser = False
        user.is_omega = True
        user.save(using=self._db)

        return user

    def create_superuser(self, uname, email, name, password):
        user = self.create_user(uname, email, name, password)

        user.is_superuser = True
        user.is_omega = True
        user.save(using=self._db)

        return user



class Users(AbstractBaseUser, PermissionsMixin):
    """ DB model for users Authentication """
    uname = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_omega = models.BooleanField(default=False)
    is_alpha = models.BooleanField(default=False)
    is_beta = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=bool(is_omega))
    objects = UsersManager()

    USERNAME_FIELD = 'uname'
    REQUIRED_FIELDS = ['email','name']

    def get_full_name(self):
        """Retrieves User's full name"""
        return self.name
    def get_short_name(self):
        """Retrieves User's full name"""
        return self.name

    def __str__(self):
        return self.uname



class FrontAuth(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)


class AuthLogs(models.Model):
    username= models.CharField(max_length=264)
    access_time = models.DateField()
    authStat = models.BooleanField()

    def __str__(self):
        return '{}{}{}'.format(self.username, str(self.authStat), str(self.access_time))
