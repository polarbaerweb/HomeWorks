from django.contrib.auth.models import AbstractUser
from django.db import models

from commerces.settings import BASE_DIR

TYPES_AUCTION = "LA", "OA", "SBA"
TYPES_AUCTIONS_TUPLE = [(TYPES_AUCTION[0], "LiveAuction"),
                        (TYPES_AUCTION[1], "OnlineAuction"),
                        (TYPES_AUCTION[2], "SealedBidAuction")]


class User(AbstractUser):
    email = models.CharField(max_length=255, default="example@gmail.com", unique=True)


class Listings(models.Model):
    title = models.CharField(max_length=255, unique=True, default="undecided")
    description = models.TextField(max_length=900, default="undecided")
    initialBids = models.DecimalField(max_digits=1_000_000, decimal_places=2)
    category = models.CharField(choices=TYPES_AUCTIONS_TUPLE, default=TYPES_AUCTIONS_TUPLE[0], max_length=255)
    image = models.ImageField(upload_to=f"{BASE_DIR}/images")
    user = models.ForeignKey("User", to_field="username", related_name="listingUser", on_delete=models.CASCADE)
    winner = models.ForeignKey("User", to_field="email", on_delete=models.CASCADE, related_name="winner", blank=True, null=True)

    class Meta:
        ordering = ["initialBids", "title"]

    def __str__(self):
        return str(self.title)


class Bid(models.Model):
    listing = models.ForeignKey("Listings", on_delete=models.CASCADE, related_name="bids", to_field="title")
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=1_000_000, decimal_places=2)

    def __str__(self):
        return str(self.listing)


class Comments(models.Model):
    listing = models.ForeignKey("Listings", on_delete=models.CASCADE, related_name="commentsItem", to_field="title")
    email = models.ForeignKey("User", on_delete=models.CASCADE, to_field="email")
    comment = models.TextField(default="undecided")

    class Meta:
        ordering = ["email"]

    def __str__(self):
        return str(self.email)


class WatchList(models.Model):
    title = models.ManyToManyField(Listings)
    user = models.OneToOneField(User, to_field="username", on_delete=models.CASCADE, null=False, blank=False)

    class Meta:
        ordering = ["user"]

    def __str__(self):
        return str(self.title)