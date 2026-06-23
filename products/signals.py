from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Payment


@receiver(post_save, sender=Payment)
def update_order_status(sender, instance, **kwargs):

    order = instance.order

    if instance.payment_status == "Verified":

        if order.status != "Processing":

            order.status = "Processing"
            order.save()

            for item in order.orderitem_set.all():

                product = item.product

                new_stock = product.stock - item.quantity

                product.stock = max(0, new_stock)

                product.save()

    elif instance.payment_status == "Rejected":

        order.status = "Cancelled"
        order.save()