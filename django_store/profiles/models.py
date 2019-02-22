from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('Email'), unique=True)
    first_name = models.CharField(_('Имя'), max_length=40)
    last_name = models.CharField(_('Фамилия'), max_length=40)
    date_joined = models.DateTimeField(_('Дата регистрации'), auto_now_add=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def get_orders(self):
        return self.customer.order_set.all()


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    discount = models.PositiveSmallIntegerField(_('Скидка'), default=0)

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def __str__(self):
        return self.user.email


@receiver(post_save, sender=User)
def create_user_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_customer(sender, instance, **kwargs):
    instance.customer.save()
