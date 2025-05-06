from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from typing import Any, Dict, Tuple


def get_default_due_date() -> timezone.datetime:
    """
    Метод для установления значения поля "срок действия"
    модели Invoice.
    """
    return timezone.now() + timedelta(minutes=1, days=5)


class InvoiceStatus(models.TextChoices):
    """
    Модель статуса счета.
    """

    PENDING = 'pending', _('Ожидает оплаты')
    PAID = 'paid', _('Оплачен')
    EXPIRED = 'expired', _('Просрочен')


class PaymentAttemptStatus(models.TextChoices):
    """
    Модель статуса попытки оплаты.
    """

    SUCCESS = 'success', _('Успешно')
    NOT_ENOUGH = 'not_enough', _('Недостаточно средств')
    REJECT = 'reject', _('Отказано')


class Invoice(models.Model):
    """
    Модель счета.
    Поля:
    - сумма
    - дата и время создания
    - статус
    - срок действия
    """

    amount: models.DecimalField = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name=_('Сумма')
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Дата и время создания')
    )
    status: models.CharField = models.CharField(
        max_length=7,
        choices=InvoiceStatus.choices,
        default=InvoiceStatus.PENDING,
        verbose_name=_('Статус'),
    )
    due_at: models.DateTimeField = models.DateTimeField(
        verbose_name=_('Срок действия до'),
        default=get_default_due_date,
    )

    class Meta:
        verbose_name = _('Счет')
        verbose_name_plural = _('Счета')

    def is_expired(self) -> bool:
        return timezone.now() > self.due_at

    def __str__(self) -> str:
        return _('Счет #{id} на {amount} руб. со статусом - {status}').format(
            id=self.id, amount=self.amount, status=self.get_status_display()
        )


class PaymentAttempt(models.Model):
    """
    Модель попытка оплаты.
    Поля:
    - вносимая сумма
    - текущие дата и время
    - результат оплаты
    - связанный счёт на оплату
    """

    income = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Вносимая сумма'))
    income_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Текущие дата и время'))
    status = models.CharField(
        choices=PaymentAttemptStatus.choices,
        max_length=10,
        verbose_name=_('Результат оплаты'),
    )
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='payment_attempts',
        verbose_name=_('Связанный счёт'),
    )

    class Meta:
        verbose_name = _('Попытка оплаты')
        verbose_name_plural = _('Попытки оплаты')

    def save(self, *args: Tuple, **kwargs: Dict[str, Any]) -> None:
        invoice = self.invoice
        if invoice.status == InvoiceStatus.EXPIRED:
            self.status = PaymentAttemptStatus.REJECT
        elif invoice.status == InvoiceStatus.PENDING:
            if self.income < invoice.amount:
                self.status = PaymentAttemptStatus.NOT_ENOUGH
            else:
                self.status = PaymentAttemptStatus.SUCCESS
                invoice.status = InvoiceStatus.PAID
                invoice.save()
        else:
            self.status = PaymentAttemptStatus.REJECT
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return _('Попытка #{id} на {income} руб. cо статусом — {status}').format(  # noqa
            id=self.id, income=self.income, status=self.get_status_display()
        )
