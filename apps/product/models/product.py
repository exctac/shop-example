from django.db import models


class Category(models.Model):
    """Модель Категория товара."""
    name = models.CharField(verbose_name='Наименование', max_length=100)
    parent = models.ForeignKey(
        'self',
        verbose_name='Родительская категория',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='children',
    )
    root = models.ForeignKey(
        'self',
        verbose_name='Корень категории',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='children_by_root',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория товара'
        verbose_name_plural = 'Категории товаров'
        indexes = [
            models.Index(fields=('parent', 'root',)),
        ]

class Product(models.Model):
    """Модель Товар."""
    name = models.CharField(verbose_name='Наименование', max_length=100)
    stock = models.PositiveIntegerField(verbose_name='Количество на складе')
    price = models.DecimalField(
        verbose_name='Цена',
        max_digits=12,
        decimal_places=2,
    )
    category = models.ForeignKey(
        'product.Category',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        indexes = [
            models.Index(fields=('category',)),
        ]
