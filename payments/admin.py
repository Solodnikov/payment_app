from django.contrib import admin

from .models import Invoice, PaymentAttempt


admin.site.register(Invoice)


@admin.register(PaymentAttempt)
class PaymentAttemptAdmin(admin.ModelAdmin):
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        return [fld for fld in fields if fld != 'status']
