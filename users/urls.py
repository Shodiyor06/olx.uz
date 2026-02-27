from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    LogoutView,
    PublicSellerView,
    SellerProductsView,
    TelegramLoginView,
    UpgradeToSellerView,
    UserMeView,
)

urlpatterns = [
    path("refresh/", TokenRefreshView.as_view()),
    path("telegram-login/", TelegramLoginView.as_view()),
    path("upgrade-to-seller/", UpgradeToSellerView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("users/me/", UserMeView.as_view()),
    path("sellers/<int:pk>/", PublicSellerView.as_view()),
    path("sellers/<int:pk>/products/", SellerProductsView.as_view()),
]
