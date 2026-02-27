from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [

    path("admin/", admin.site.urls),

    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema")),

    path("api/v1/", include("users.urls")),
    path("api/v1/", include("products.urls")),
    path("api/v1/", include("orders.urls")),
    path("api/v1/telegram/", include("telegram_auth.urls")),
]