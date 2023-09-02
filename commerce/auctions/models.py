from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Category(models.Model):
    title = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.title}"

class Listing_item(models.Model):
    title = models.CharField(max_length = 64)
    description = models.TextField()
    starting_bid = models.IntegerField()
    picture = models.CharField(max_length = 1000, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    isActive = models.BooleanField(default=True)
    watchlist = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="users")

    def __str__(self):
        return f"{self.title}, {self.category}, {self.isActive}"

class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment_author")
    listing_item_id = models.ForeignKey(Listing_item, on_delete=models.CASCADE, related_name="comments")