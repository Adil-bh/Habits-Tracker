from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext as _


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not email:
            return ValueError(_("You have to enter an email"))
        user = self.model(
            email=self.normalize_email(email),
        )
        user.username = username
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None):
        user = self.create_user(username=username, email=email, password=password)
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user


class CustomUser(AbstractBaseUser):
    username = models.CharField(unique=True, max_length=15, blank=False)
    first_name = models.CharField()
    last_name = models.CharField()
    email = models.EmailField(unique=True, max_length=255, blank=False)

    # User status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]
    objects = CustomUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class Tasks(models.Model):
    name = models.CharField(blank=False)


class Habits(models.Model):
    name = models.CharField()
    tasks = models.ForeignKey(Tasks, null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    users_id = models.ManyToManyField(CustomUser)
    created_at = models.DateTimeField(auto_now=True)