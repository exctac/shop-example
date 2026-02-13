from django.db import models


class Order(models.Model):
    """Модель Заказ."""
    customer = models.ForeignKey(
        'customer.Customer',
        verbose_name='Клиент',
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
    )
    created_at = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True,
    )

    def __str__(self):
        return f"Заказ #{self.pk} — {self.customer}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        indexes = [
            models.Index(fields=('customer', 'created_at',)),
        ]


class OrderItem(models.Model):
    """Модель Позиция в заказе."""
    product = models.ForeignKey(
        'product.Product',
        verbose_name='Товар',
        on_delete=models.DO_NOTHING,
        related_name='+',
    )
    order = models.ForeignKey(
        'order.Order',
        verbose_name='Заказ',
        on_delete=models.CASCADE,
        related_name='items',
    )
    quantity = models.PositiveIntegerField(verbose_name='Количество товаров')
    price = models.DecimalField(
        verbose_name='Цена товара',
        help_text='Цена на момент заказа',
        max_digits=12,
        decimal_places=2,
    )

    def __str__(self):
        return f'Позиция заказа {self.order}'

    class Meta:
        verbose_name = 'Позиция заказа'
        verbose_name_plural = 'Позиции заказов'
        indexes = [
            models.Index(fields=('product', 'order',)),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=('order', 'product',),
                name='unique_order_product'
            )
        ]
