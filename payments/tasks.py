from celery import shared_task
from django.utils import timezone

from .models import Invoice, InvoiceStatus


@shared_task
def expire_invoice(invoice_id: int) -> None:
    """
    Фоновая задача для перевода счёта в статус 'Просрочен'.

    Получает счёт по ID и проверяет:
    - существует ли он;
    - находится ли он в статусе "Ожидает оплаты";
    - истёк ли срок его действия (due_at < текущее время).

    Если все условия выполнены, счёт переводится в статус 'Просрочен'.

    :param invoice_id: Идентификатор счёта, подлежащего проверке.
    :return: None
    """
    try:
        invoice = Invoice.objects.get(id=invoice_id)
    except Invoice.DoesNotExist:
        return None

    if invoice.status == InvoiceStatus.PENDING and (timezone.now() > invoice.due_at):
        invoice.status = InvoiceStatus.EXPIRED
        invoice.save()
