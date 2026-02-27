from django.urls import path

from .views import (
    CreateReviewView,
    OrderDetailView,
    OrderListCreateView,
    ReviewListView,
)

urlpatterns = [

    path("orders/", OrderListCreateView.as_view()),
    path("orders/<int:pk>/", OrderDetailView.as_view()),

    path("reviews/", ReviewListView.as_view()),
    path("reviews/create/", CreateReviewView.as_view()),
]