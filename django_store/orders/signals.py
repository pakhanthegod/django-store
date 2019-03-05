from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import OrderList


@receiver(post_save, sender=OrderList)
def decrement_products(sender, instance, **kwargs):
    print(instance.product.decrease_quantity)
    print(instance.quantity)
    print('qqqq')
    instance.product.decrease_quantity(instance.quantity)
