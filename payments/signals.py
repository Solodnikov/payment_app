# payment/signals.py

# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from django.utils.timezone import now
# from datetime import timedelta

# from .models import Invoice, InvoiceStatus
# from .tasks import expire_invoice


# @receiver(post_save, sender=Invoice)
# def schedule_expiry_task(sender, instance: Invoice, created: bool, **kwargs) -> None:
#     if created and instance.status == InvoiceStatus.PENDING:
#         delay = (instance.due_at - now()).total_seconds()
#         expire_invoice.apply_async((instance.id,), countdown=delay)
# payment_app/payments/signals.py


from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Invoice
from .tasks import notify_invoice_created


@receiver(post_save, sender=Invoice)
def invoice_created_handler(sender, instance, created, **kwargs):
    if created:
        notify_invoice_created.delay(instance.id)