from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Invoice, InvoiceStatus
from .tasks import expire_invoice


@receiver(post_save, sender=Invoice)
def schedule_expiry_task(sender, instance: Invoice, created: bool, **kwargs) -> None:
    """
    Сигнал, запускаемый после создания счёта.

    Если счёт создан и его статус — 'Ожидает оплаты',
    планирует выполнение фоновой задачи `expire_invoice`
    через промежуток времени, равный сроку действия счёта (due_at - now).

    :param sender: Модель, отправившая сигнал (Invoice).
    :param instance: Экземпляр модели Invoice.
    :param created: Флаг, указывающий, создан ли объект (True) или обновлён (False).
    :param kwargs: Дополнительные аргументы сигнала.
    :return: None
    """
    if created and instance.status == InvoiceStatus.PENDING:
        delay = (instance.due_at - timezone.now()).total_seconds()
        expire_invoice.apply_async((instance.id,), countdown=delay)
