from django.urls import path
from .views import (
    CreateOrderView,
    MyOrdersView,
    AgreeOrderView,
    CompleteOrderView,
    OrderListCreateView,
    OrderDetailView,
    ReviewListView,
    CreateReviewView,
)

urlpatterns = [

    path("orders/", OrderListCreateView.as_view()),
    path("orders/create/", CreateOrderView.as_view()),
    path("orders/<int:pk>/", OrderDetailView.as_view()),

    path("orders/<int:pk>/agree/", AgreeOrderView.as_view()),
    path("orders/<int:pk>/complete/", CompleteOrderView.as_view()),

    path("reviews/", ReviewListView.as_view()),
    path("reviews/create/", CreateReviewView.as_view()),
]