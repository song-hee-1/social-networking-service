from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('이메일은 필수로 입력해야 합니다.')
        email = self.normalize_email(email)
        if not username:
            raise ValueError('이름은 필수로 입력해야 합니다.')
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser is_staff=True이어야 합니다.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser is_superuser=True이어야 합니다.')
        return self.create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    username = models.CharField(max_length=40, unique=False)
    email = models.EmailField(unique=True, max_length=250)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    class Meta:
        verbose_name = "사용자"
        verbose_name_plural = "사용자 목록"
        db_table = "user"

    def __str__(self):
        return self.email
