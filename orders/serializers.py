from rest_framework import serializers

from .models import Order, Review


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["buyer", "seller", "status"]


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["reviewer", "seller"]


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["buyer", "seller", "final_price"]
