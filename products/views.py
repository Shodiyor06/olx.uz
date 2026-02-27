from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsSeller

from .models import Category, Favorite, Product
from .serializers import (
    CategorySerializer,
    FavoriteSerializer,
    ProductImageSerializer,
    ProductSerializer,
)


class ProductCreateView(generics.CreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsSeller]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.filter(status="active")


class ProductDetailView(APIView):

    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk, status="active")

        product.view_count += 1
        product.save()

        serializer = ProductSerializer(product)
        return Response(serializer.data)


class ProductUpdateView(generics.UpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsSeller]

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)


class ProductDeleteView(generics.DestroyAPIView):
    permission_classes = [IsSeller]

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)


class PublishProductView(APIView):
    permission_classes = [IsSeller]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk, seller=request.user)

        product.status = "active"
        product.save()

        return Response({"message": "Product published"})


class UploadProductImageView(APIView):
    permission_classes = [IsSeller]
    parser_classes = [MultiPartParser]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk, seller=request.user)

        serializer = ProductImageSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data)

        return Response(serializer.errors, status=400)


class AddFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        product_id = request.data.get("product_id")

        favorite, created = Favorite.objects.get_or_create(
            user=request.user, product_id=product_id
        )

        return Response({"message": "Added to favorites"})


class FavoriteListView(generics.ListAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


class RemoveFavoriteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        fav = get_object_or_404(Favorite, pk=pk, user=request.user)
        fav.delete()

        return Response({"message": "Removed"})


class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]


    filterset_fields = ["category", "region"]


    search_fields = ["title", "description"]


    ordering_fields = ["price", "created_at", "view_count"]

    def get_queryset(self):
        queryset = Product.objects.filter(status="active")


        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset


class CategoryListView(ListAPIView):
    queryset = Category.objects.filter(parent=None, is_active=True)
    serializer_class = CategorySerializer


class CategoryDetailView(RetrieveAPIView):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = "slug"


class CategoryProductsView(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        slug = self.kwargs["slug"]

        category = Category.objects.get(slug=slug)

        return Product.objects.filter(category=category, status="active")