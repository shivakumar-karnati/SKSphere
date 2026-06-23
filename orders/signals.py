from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Payment


@receiver(post_save, sender=Payment)
def update_order_status(sender, instance, **kwargs):

    order = instance.order

    if instance.payment_status == "Verified":

        order.status = "Processing"

        order.save()

    elif instance.payment_status == "Rejected":

        order.status = "Cancelled"

        order.save()