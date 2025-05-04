from .admin import unfold_admin_site
from django.urls import path

urlpatterns = [
    path('', unfold_admin_site.urls),
]
