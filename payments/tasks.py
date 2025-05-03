# from celery import shared_task
# from django.utils import timezone

# from .models import Invoice, InvoiceStatus


# @shared_task
# def expire_invoice(invoice_id: int) -> None:
#     # from payments.models import Invoice  # защита от circular import

#     try:
#         invoice = Invoice.objects.get(id=invoice_id)
#     except Invoice.DoesNotExist:
#         return  # ничего не делать, если счёт удалён

#     if invoice.status == InvoiceStatus.PENDING and timezone.now() > invoice.due_at:
#         invoice.status = InvoiceStatus.EXPIRED
#         invoice.save()

from celery import shared_task
from .models import Invoice


@shared_task
def debug_task():
    print("Celery работает!")
    return "OK"


@shared_task
def notify_invoice_created(invoice_id: int):
    try:
        invoice = Invoice.objects.get(id=invoice_id)
        print(f"Создан новый счет #{invoice.id} на сумму {invoice.amount}")
        # Тут можно реализовать уведомление, проверку срока, запись в лог и т.д.
    except Invoice.DoesNotExist:
        print(f"Счет с ID {invoice_id} не найден.")
