from django.db import models
from account.managers import UserManager
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _


class User(AbstractBaseUser):
    phone = models.CharField(
        verbose_name=_('phone'),
        max_length=11,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'phone'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Otp(models.Model):
    phone = models.CharField(max_length=11, verbose_name='شماره تلفن')
    code = models.SmallIntegerField(verbose_name='کد ارسال شده')
    token = models.CharField(max_length=200, null=True, blank=True, verbose_name='توکن')

    def __str__(self):
        return self.phone


class Profile(models.Model):
    phone = models.ForeignKey(User, on_delete=models.CASCADE,verbose_name='شماره تلفن')
    name = models.CharField(max_length=50,verbose_name='نام')
    last_name = models.CharField(max_length=200,verbose_name='نام خانوادگی')
    birthday = models.DateField(verbose_name='تاریخ تولد')
    melicode = models.PositiveIntegerField( unique=True,verbose_name='کد ملی')
    bank = models.PositiveIntegerField(unique=True,verbose_name='شماره کارت')

    def __str__(self):
        return f'{self.name}-{self.phone}'

