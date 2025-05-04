from celery import shared_task
from django.utils import timezone

from .models import Invoice, InvoiceStatus


@shared_task
def expire_invoice(invoice_id: int) -> None:
    try:
        invoice = Invoice.objects.get(id=invoice_id)
    except Invoice.DoesNotExist:
        return  # ничего не делать, если счёт удалён

    if invoice.status == InvoiceStatus.PENDING and (
                timezone.now() > invoice.due_at):
        invoice.status = InvoiceStatus.EXPIRED
        invoice.save()
