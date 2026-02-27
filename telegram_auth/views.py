from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User

from .models import TelegramLoginCode


class TelegramBotLoginView(APIView):

    def post(self, request):
        telegram_id = request.data.get("telegram_id")
        phone_number = request.data.get("phone_number")
        first_name = request.data.get("first_name")

        user, created = User.objects.get_or_create(
            telegram_id=telegram_id,
            defaults={
                "username": f"user_{telegram_id}",
                "first_name": first_name,
                "phone_number": phone_number,
            },
        )

        login_code = TelegramLoginCode.objects.create(user=user)
        login_code.generate_code()

        return Response({"code": login_code.code})


from rest_framework_simplejwt.tokens import RefreshToken


class VerifyTelegramCodeView(APIView):

    def post(self, request):
        code = request.data.get("code")

        login_code = TelegramLoginCode.objects.filter(code=code, is_used=False).first()

        if not login_code:
            return Response({"error": "Invalid code"}, status=400)

        if login_code.is_expired():
            return Response({"error": "Code expired"}, status=400)

        login_code.is_used = True
        login_code.save()

        refresh = RefreshToken.for_user(login_code.user)

        return Response({"access": str(refresh.access_token), "refresh": str(refresh)})
