from django.contrib import admin
from unfold.admin import ModelAdmin

from payments.models import Invoice, PaymentAttempt
from unfold_admin.sites import unfold_admin_site
from payments.admin import BaseInvoiceAdmin, BasePaymentAttemptAdmin


@admin.register(Invoice, site=unfold_admin_site)
class InvoiceUnfoldAdmin(BaseInvoiceAdmin, ModelAdmin):
    """
    Кастомная админка Unfold для модели Invoice.

    Наследует всю логику отображения и форматирования
    из BaseInvoiceAdmin, но регистрируется в кастомном интерфейсе Unfold.
    """

    pass


@admin.register(PaymentAttempt, site=unfold_admin_site)
class PaymentAttemptUnfoldAdmin(BasePaymentAttemptAdmin, ModelAdmin):
    """
    Кастомная админка Unfold для модели PaymentAttempt.

    Повторно использует базовую логику отображения и регистрации,
    но в рамках интерфейса Unfold.
    """

    pass
