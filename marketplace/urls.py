from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),
    # Swagger schema
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    # Swagger UI
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
    # API lar
    path("api/v1/", include("users.urls")),
    path("api/v1/", include("products.urls")),
    path("api/v1/", include("orders.urls")),
    path("api/v1/telegram/", include("telegram_auth.urls")),
]
