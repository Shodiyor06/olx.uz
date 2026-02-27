from django.urls import path

from .views import TelegramBotLoginView, VerifyTelegramCodeView

urlpatterns = [
    path("bot-login/", TelegramBotLoginView.as_view()),
    path("verify-code/", VerifyTelegramCodeView.as_view()),
]
