from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from .utils import send_custom_email
from django.utils.translation import gettext as _

class UserManager(BaseUserManager):
    def create_user(self,email,full_name,password,how_meet):

        if not email:
            raise ValueError('user must have email number')

        if not full_name:
            raise ValueError('user must have full_name number')

        if not password:
            raise ValueError('user must have password number')


        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            how_meet=how_meet
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,full_name,password):
        if not email:
            raise ValueError('user must have email number')

        if not full_name:
            raise ValueError('user must have full_name number')

        if not password:
            raise ValueError('user must have password number')


        user = self.model(
            email=self.normalize_email(email),
            full_name=full_name,
            is_admin=True,
            is_email_active=True,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    FIND_CHOICE = [
        ('fri',_('Firnd')),
        ('goo',_('Google')),
        ('soc',_('social')),
        ('oth',_('other')),
    ]

    full_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    how_meet = models.CharField(max_length=5,choices=FIND_CHOICE,verbose_name="How did you find out about the website?",blank=True,null=True)
    phone_number = models.CharField(max_length=15,blank=True,null=True)
    is_admin = models.BooleanField(default=False)
    is_email_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['full_name',]

    def __str__(self):
        return self.full_name

    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def send_email(self,subject,message):
        send_custom_email(self.email,subject,message)