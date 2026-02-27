from django.conf import settings
from django.db import models

from products.models import Product


class Order(models.Model):

    STATUS_CHOICES = (
        ("waiting", "Waiting"),
        ("agreed", "Agreed"),
        ("done", "Done"),
        ("cancelled", "Cancelled"),
    )

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="buyer_orders", on_delete=models.CASCADE
    )

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="seller_orders", on_delete=models.CASCADE
    )

    final_price = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="waiting")

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id}"


class Review(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)

    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="reviews", on_delete=models.CASCADE
    )

    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.seller}"
