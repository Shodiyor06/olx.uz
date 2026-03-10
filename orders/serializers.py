from rest_framework import serializers

from .models import Order, Review

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["product", "notes"]

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = ["buyer", "seller", "final_price", "status"]

class ReviewSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["reviewer", "seller"]