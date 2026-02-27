from django.urls import path

from .views import *

urlpatterns = [
    # PRODUCTS
    path("products/", ProductListView.as_view()),
    path("products/create/", ProductCreateView.as_view()),
    path("products/<int:pk>/", ProductDetailView.as_view()),
    path("products/<int:pk>/update/", ProductUpdateView.as_view()),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view()),
    path("products/<int:pk>/publish/", PublishProductView.as_view()),
    path("products/<int:pk>/upload-image/", UploadProductImageView.as_view()),
    # FAVORITES
    path("favorites/", FavoriteListView.as_view()),
    path("favorites/add/", AddFavoriteView.as_view()),
    path("favorites/<int:pk>/delete/", RemoveFavoriteView.as_view()),
    # CATEGORIES
    path("categories/", CategoryListView.as_view()),
    path("categories/<slug:slug>/", CategoryDetailView.as_view()),
    path("categories/<slug:slug>/products/", CategoryProductsView.as_view()),
]
