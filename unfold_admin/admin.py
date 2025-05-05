from django.contrib import admin
from unfold.admin import ModelAdmin

from payments.models import Invoice, PaymentAttempt
from unfold_admin.sites import unfold_admin_site
from django.utils.html import format_html


# TODO: может сделать общий класс и для джанго админки
@admin.register(Invoice, site=unfold_admin_site)
class InvoiceUnfoldAdmin(ModelAdmin):
    list_display = ("id", "amount", "colored_status", "created_at", "due_at")
    list_filter = ("status",)
    search_fields = ("id",)
    ordering = ("-created_at",)

    def get_fields(self, request, obj=None):
        """Убираем status из формы создания"""
        fields = super().get_fields(request, obj)
        if obj is None:
            return [fld for fld in fields if fld != "status"]
        return fields

    def colored_status(self, obj):
        color_map = {
            'pending': 'orange',
            'paid': 'green',
            'expired': 'red',
        }
        color = color_map.get(obj.status, 'gray')
        return format_html(
            '<span style="color: white; background-color: {}; padding: 2px 8px; border-radius: 4px;">{}</span>', # noqa
            color, obj.get_status_display()
        )
    colored_status.short_description = "Статус"


@admin.register(PaymentAttempt, site=unfold_admin_site)
class PaymentAttemptUnfoldAdmin(ModelAdmin):
    list_display = ("id", "invoice", "income", "colored_status", "income_at")
    list_filter = ("status",)
    search_fields = ("id", "invoice__id")
    ordering = ("-income_at",)

    def get_fields(self, request, obj=None):
        """Убираем status из формы создания"""
        fields = super().get_fields(request, obj)
        if obj is None:
            return [fld for fld in fields if fld != "status"]
        return fields

    def colored_status(self, obj):
        color_map = {
            'success': 'green',
            'reject': 'red',
            'not_enough': 'orange',
        }
        color = color_map.get(obj.status, 'gray')
        return format_html(
            '<span style="color: white; background-color: {}; padding: 2px 8px; border-radius: 4px;">{}</span>', # noqa
            color, obj.get_status_display()
        )
    colored_status.short_description = "Статус"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "invoice":
            kwargs["queryset"] = Invoice.objects.filter(status="pending")
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
