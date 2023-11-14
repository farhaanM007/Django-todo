from typing import Any
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

class CustomUserManager(BaseUserManager):
    def create_user(self,email,password,**kwargs):
        email=self.normalize_email(email)

        user= self.model(
            email=email,
            **kwargs
        )

        user.set_password(password)

        user.save()

        return user

    def create_superuser(self,email,password,**kwargs):

        kwargs.setdefault("is_staff",True)
        kwargs.setdefault("is_superuser",True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser has to be is_staff being True")
        
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser has to be is_superuser being True")
        
        return self.create_user(password=password,email=email,**kwargs)
    

class User(AbstractUser):
    email=models.CharField(max_length=50,unique=True)
    username=models.CharField(max_length=50)
    date_of_birth=models.DateField(null=True)

    objects=CustomUserManager()

    USERNAME_FIELD="email"

    REQUIRED_FIELDS=["username"]

    def __str__(self):
        return self.username



