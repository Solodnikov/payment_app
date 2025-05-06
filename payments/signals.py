from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Invoice, InvoiceStatus
from .tasks import expire_invoice


@receiver(post_save, sender=Invoice)
def schedule_expiry_task(sender, instance: Invoice, created: bool, **kwargs) -> None:  # noqa
    if created and instance.status == InvoiceStatus.PENDING:
        delay = (instance.due_at - timezone.now()).total_seconds()
        expire_invoice.apply_async((instance.id,), countdown=delay)
