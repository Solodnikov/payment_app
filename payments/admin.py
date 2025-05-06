from typing import List
from django.contrib import admin
from django.utils.html import format_html
from .models import Invoice, PaymentAttempt


class BaseInvoiceAdmin(admin.ModelAdmin):
    """
    Базовая админка для модели Invoice.

    Отображает ключевые поля счета, добавляет фильтрацию и поиск,
    а также цветовую метку для отображения статуса.
    """
    list_display = ('id', 'amount', 'colored_status', 'created_at', 'due_at')
    list_filter = ('status',)
    search_fields = ('id',)
    ordering = ('-created_at',)

    def get_fields(self, request, obj=None) -> List[str]:
        """
        Удаляет поле 'status' из формы создания счета.
        При редактировании счетов поле отображается.
        """
        fields = super().get_fields(request, obj)
        if obj is None:
            return [fld for fld in fields if fld != 'status']
        return fields

    def colored_status(self, obj: Invoice) -> str:
        """
        Отображает статус счета с цветовой меткой для наглядности.
        """
        color_map = {
            'pending': 'orange',
            'paid': 'green',
            'expired': 'red',
        }
        color = color_map.get(obj.status, 'gray')
        return format_html(
            '<span style="color: white; background-color: {}; padding: 2px 8px; border-radius: 4px;">{}</span>',  # noqa
            color,
            obj.get_status_display(),
        )

    colored_status.short_description = 'Статус'


class BasePaymentAttemptAdmin(admin.ModelAdmin):
    """
    Базовая админка для модели PaymentAttempt.

    Отображает данные о попытках оплаты, включая цветовую метку статуса.
    Фильтрует доступные счета при создании попытки.
    """
    list_display = ('id', 'invoice', 'income', 'colored_status', 'income_at')
    list_filter = ('status',)
    search_fields = ('id', 'invoice__id')
    ordering = ('-income_at',)

    def get_fields(self, request, obj=None) -> List[str]:
        """
        Удаляет поле 'status' из формы создания попытки оплаты.
        При редактировании поле отображается.
        """
        fields = super().get_fields(request, obj)
        if obj is None:
            return [fld for fld in fields if fld != 'status']
        return fields

    def colored_status(self, obj: PaymentAttempt) -> str:
        color_map = {
            'success': 'green',
            'reject': 'red',
            'not_enough': 'orange',
        }
        color = color_map.get(obj.status, 'gray')
        return format_html(
            '<span style="color: white; background-color: {}; padding: 2px 8px; border-radius: 4px;">{}</span>',  # noqa
            color,
            obj.get_status_display(),
        )

    colored_status.short_description = 'Статус'

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Ограничивает выбор счетов только теми, которые находятся в статусе 'pending'.
        Используется при создании новой попытки оплаты.
        """
        if db_field.name == 'invoice':
            kwargs['queryset'] = Invoice.objects.filter(status='pending')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Invoice)
class InvoiceAdmin(BaseInvoiceAdmin):
    """
    Регистрация модели Invoice в админке.
    """
    pass


@admin.register(PaymentAttempt)
class PaymentAttemptAdmin(BasePaymentAttemptAdmin):
    """
    Регистрация модели PaymentAttempt в админке.
    """
    pass
