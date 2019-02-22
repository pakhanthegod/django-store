from django.db import models
from django.utils.translation import ugettext_lazy as _

from profiles.models import Customer
from products.models import Product


class Order(models.Model):
    ORDER_PROCESS = 'process'
    ORDER_SHIPPED = 'shipped'
    ORDER_DELIVERED = 'delivered'

    ORDER_STATUS_CHOICES = (
        (ORDER_PROCESS, 'Обрабатывается'),
        (ORDER_SHIPPED, 'Отправлено', ),
        (ORDER_DELIVERED, 'Доставлено'),
    )

    customer = models.ForeignKey(verbose_name=_('Покупатель'), to=Customer, on_delete=models.CASCADE)
    order_status = models.CharField(_('Статус'), max_length=20, default=ORDER_PROCESS, choices=ORDER_STATUS_CHOICES)
    order_date = models.DateTimeField(_('Дата заказа'), auto_now_add=True)
    products = models.ManyToManyField(verbose_name=_('Товары'), to=Product, through='OrderList')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.id)

    def get_total(self):
        total = 0
        
        for ol in self.orderlist_set.all():
            total += ol.get_sum()
        
        return total


class OrderList(models.Model):
    order = models.ForeignKey(verbose_name=_('Заказ'), to=Order, on_delete=models.CASCADE)
    product = models.ForeignKey(verbose_name=_('Товар'), to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(_('Количество'), default=1)

    class Meta:
        verbose_name = 'Товары заказа'
        verbose_name_plural = 'Товары заказа'

    def get_sum(self):
        return self.product.price * self.quantity