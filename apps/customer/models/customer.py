from django.db import models


class Customer(models.Model):
    """Модель Клиент."""
    name = models.CharField(verbose_name='Наименование', max_length=100)
    address = models.CharField(verbose_name='Адрес', max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
