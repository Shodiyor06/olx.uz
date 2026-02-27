from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import Product

from .models import Order, Review
from .serializers import OrderSerializer, ReviewSerializer


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")

        product = get_object_or_404(Product, id=product_id)

        # 🔥 MUHIM TEKSHIRUV
        if not product.price:
            return Response({"error": "Product price not set"}, status=400)

        order = Order.objects.create(
            product=product,
            buyer=request.user,
            seller=product.seller,
            final_price=product.price,
        )

        return Response({"message": "Order created", "order_id": order.id})


class MyOrdersView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user)


class AgreeOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, seller=request.user)

        order.status = "agreed"
        order.save()

        return Response({"message": "Order agreed"})


class CompleteOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, buyer=request.user)

        order.status = "done"
        order.save()

        # Product sotilgan bo‘ladi
        order.product.status = "sold"
        order.product.save()

        return Response({"message": "Order completed"})


class CreateReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")
        rating = request.data.get("rating")
        comment = request.data.get("comment")

        order = get_object_or_404(Order, id=order_id)

        # 🔥 tekshiruvlar
        if order.buyer != request.user:
            return Response({"error": "Not your order"}, status=403)

        if order.status != "done":
            return Response({"error": "Order not completed"}, status=400)

        # review yaratish
        review = Review.objects.create(
            order=order,
            reviewer=request.user,
            seller=order.seller,
            rating=rating,
            comment=comment,
        )

        # ⭐ seller ratingni yangilaymiz
        reviews = Review.objects.filter(seller=order.seller)
        avg_rating = sum(r.rating for r in reviews) / reviews.count()

        seller_profile = order.seller.sellerprofile
        seller_profile.rating = avg_rating
        seller_profile.save()

        return Response({"message": "Review added"})


class OrderListCreateView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        role = self.request.query_params.get("role")

        if role == "seller":
            return Order.objects.filter(seller=self.request.user)

        return Order.objects.filter(buyer=self.request.user)

    def perform_create(self, serializer):
        product_id = self.request.data.get("product_id")
        product = get_object_or_404(Product, id=product_id)

        serializer.save(
            buyer=self.request.user, seller=product.seller, final_price=product.price
        )


class OrderDetailView(RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user) | Order.objects.filter(
            seller=self.request.user
        )

    def perform_update(self, serializer):
        order = self.get_object()
        user = self.request.user
        new_status = self.request.data.get("status")

        # Seller status o‘zgartiradi
        if user == order.seller:
            if new_status in ["agreed", "cancelled"]:
                serializer.save(status=new_status)

        # Buyer sotib oldi
        elif user == order.buyer:
            if new_status == "done":
                serializer.save(status="done")

                # product sotildi
                order.product.status = "sold"
                order.product.save()


class ReviewListView(ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        seller_id = self.request.query_params.get("seller_id")

        if seller_id:
            return Review.objects.filter(seller_id=seller_id)

        return Review.objects.all()
