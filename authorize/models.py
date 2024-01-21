from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models


class CustomUser(AbstractUser):
    avatar = models.ImageField('Аватар', upload_to='serveruploads',
                               default='serveruploads/placeholder.jpg')
    address = models.CharField(verbose_name='Адресс проживания', max_length=255, blank=True, null=True)
    phone_number = models.CharField(verbose_name='Номер телефона', max_length=12, null=True)
    birthday = models.DateField(verbose_name='Дата рождения', null=True, blank=True)

    groups = models.ManyToManyField(Group, related_name='customuser_set', blank=True, verbose_name='Groups')

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
        verbose_name='User permissions',
        help_text='Specific permissions for this user.',
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = 'Пользователи системы'
