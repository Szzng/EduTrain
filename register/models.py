from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.db import models
from django.utils import timezone
from course.models import Category

class MyUserManager(BaseUserManager):
    def create_user(self, email, nickname, password, interest):
        if not email:
            raise ValueError('이메일 주소를 입력해주세요.')
        user = self.model(email=self.normalize_email(email), nickname=nickname, interest=interest)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nickname, password):
        user = self.create_user(email=email, password=password, nickname=nickname,)
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True,)
    nickname = models.CharField(max_length=30, unique=True,)
    date_joined = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    interest = models.ManyToManyField(Category)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nickname', 'interest', ]

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        return self.is_admin
