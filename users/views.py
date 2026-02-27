from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from products.models import Product
from products.serializers import ProductSerializer

from .models import SellerProfile, User
from .serializers import SellerProfileSerializer, UserMeSerializer
from .utils import check_telegram_auth


class TelegramLoginView(APIView):

    def post(self, request):
        data = request.data.copy()

        # 1️⃣ Hash tekshiramiz
        TEST_MODE = True

        if not TEST_MODE:
            if not check_telegram_auth(data):
                return Response({"error": "Invalid Telegram login"}, status=403)

        # 2️⃣ User yaratamiz yoki topamiz
        user, created = User.objects.get_or_create(
            telegram_id=data["id"],
            defaults={
                "username": data.get("username"),
                "first_name": data.get("first_name"),
                "last_name": data.get("last_name", ""),
            },
        )

        # 3️⃣ JWT token beramiz
        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            }
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response({"message": "Logged out"})


class UserMeView(RetrieveUpdateAPIView):
    serializer_class = UserMeSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class PublicSellerView(RetrieveAPIView):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer


class UpgradeToSellerView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        if user.role == "seller":
            return Response({"error": "Already seller"}, status=400)

        shop_name = request.data.get("shop_name")
        region = request.data.get("region")
        district = request.data.get("district")

        SellerProfile.objects.create(
            user=user,
            shop_name=shop_name,
            region=region,
            district=district,
        )

        user.role = "seller"
        user.save()

        return Response({"message": "Now you are seller"})


class SellerProductsView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        seller_id = self.kwargs["pk"]
        return Product.objects.filter(seller_id=seller_id, status="active")
