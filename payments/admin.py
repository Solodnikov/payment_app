from django.contrib import admin

from .models import PaymentAttempt, Invoice

admin.site.register([PaymentAttempt, Invoice])
