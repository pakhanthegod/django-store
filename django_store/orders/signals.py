from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import OrderList


@receiver(post_save, sender=OrderList)
def decrement_products(sender, instance, created, **kwargs):
    if created:
        instance.product.decrease_quantity(instance.quantity)
