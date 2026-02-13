from django.db import transaction
from django.db.models import F
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404

from apps.order.models import Order, OrderItem
from apps.product.models import Product
from .serializers import AddOrderItemQuerySerializer, OrderItemSerializer


class OrderItemsApiView(APIView):
    """Представление API для управления элементами заказа.

    Предоставляет возможности для добавления элементов в заказ.
    Выполняет проверку наличия продуктов на складе, обновляет запасы продуктов
    и управляет количеством элементов заказа. Все операции заключены
    в транзакцию базы данных для обеспечения целостности данных.

    Методы:
        post: Добавляет товар в заказ.
        * Возможно расширение в будущем для удаления товара из заказа
        через DELETE-запрос.
    """

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """Добавляет товар в заказ.

        Обязательные параметры в теле запроса:
            - product_id - id товара
            - quantity - количество товара

        :return: Ответ с данными о добавленном товаре в заказ или
        сообщение об ошибке.
        """

        order = get_object_or_404(Order, id=kwargs['order_id'])

        serializer = AddOrderItemQuerySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product, id=serializer.validated_data['product_id'])
        quantity = serializer.validated_data['quantity']

        updated = (
            Product.objects
            .filter(id=product.id, stock__gte=quantity)
            .update(stock=F('stock') - quantity)
        )

        if updated == 0:
            return Response(
                {'detail': 'Недостаточно товаров.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        order_item, created = OrderItem.objects.get_or_create(
            order=order,
            product_id=product.id,
            defaults={'quantity': quantity, 'price': product.price},
        )

        if not created:
            OrderItem.objects.filter(id=order_item.id).update(
                quantity=F('quantity') + quantity
            )
            order_item.refresh_from_db()

        return Response(
            OrderItemSerializer(instance=order_item).data,
            status=status.HTTP_201_CREATED,
        )
