from django.contrib import admin
from unfold.admin import ModelAdmin

from payments.models import Invoice, PaymentAttempt
from unfold_admin.sites import unfold_admin_site
from payments.admin import BaseInvoiceAdmin, BasePaymentAttemptAdmin


@admin.register(Invoice, site=unfold_admin_site)
class InvoiceUnfoldAdmin(BaseInvoiceAdmin, ModelAdmin):
    pass


@admin.register(PaymentAttempt, site=unfold_admin_site)
class PaymentAttemptUnfoldAdmin(BasePaymentAttemptAdmin, ModelAdmin):
    pass
