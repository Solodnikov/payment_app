# from unfold.admin import ModelAdmin
# from unfold.sites import UnfoldAdminSite
# from payments.models import Invoice, PaymentAttempt


# class CustomUnfoldAdminSite(UnfoldAdminSite):
#     site_header = "Unfold Admin Panel"
#     site_title = "Unfold Admin"
#     index_title = "Добро пожаловать в Unfold админку"


# # Создаем экземпляр кастомной админки Unfold
# unfold_admin_site = CustomUnfoldAdminSite(name='unfold_admin')


# class InvoiceUnfoldAdmin(ModelAdmin):
#     list_display = ("id", "amount", "status", "created_at", "due_at")
#     list_filter = ("status",)
#     search_fields = ("id",)
#     ordering = ("-created_at",)


# class PaymentAttemptUnfoldAdmin(ModelAdmin):
#     list_display = ("id", "invoice", "income", "status", "income_at")
#     list_filter = ("status",)
#     search_fields = ("id", "invoice__id")
#     ordering = ("-income_at",)


# unfold_admin_site.register(Invoice, InvoiceUnfoldAdmin)
# unfold_admin_site.register(PaymentAttempt, PaymentAttemptUnfoldAdmin)

from django.contrib import admin
from unfold.admin import ModelAdmin

from payments.models import Invoice
from unfold_admin.sites import new_admin_site


@admin.register(Invoice, site=new_admin_site)
class UnfoldYourModelAdmin(ModelAdmin):
    pass
