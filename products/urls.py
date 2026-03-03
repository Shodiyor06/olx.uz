from django.urls import path

from .views import (
    MyProductsView,
    ProductListView,
    ProductCreateView,
    ProductDetailView,
    ProductUpdateView,
    ProductDeleteView,
    PublishProductView,
    UploadProductImageView,
    FavoriteListView,
    AddFavoriteView,
    RemoveFavoriteView,
    CategoryListView,
    CategoryDetailView,
    CategoryProductsView,)

urlpatterns = [
    path("products/my/", MyProductsView.as_view()),
    path("products/", ProductListView.as_view()),
    path("products/create/", ProductCreateView.as_view()),
    path("products/<int:pk>/", ProductDetailView.as_view()),
    path("products/<int:pk>/update/", ProductUpdateView.as_view()),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view()),
    path("products/<int:pk>/publish/", PublishProductView.as_view()),
    path("products/<int:pk>/upload-image/", UploadProductImageView.as_view()),

    path("favorites/", FavoriteListView.as_view()),
    path("favorites/add/", AddFavoriteView.as_view()),
    path("favorites/<int:pk>/delete/", RemoveFavoriteView.as_view()),

    path("categories/", CategoryListView.as_view()),
    path("categories/<slug:slug>/", CategoryDetailView.as_view()),
    path("categories/<slug:slug>/products/", CategoryProductsView.as_view()),
]