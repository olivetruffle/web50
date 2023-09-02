from django.contrib import admin
from .models import User, Listing_item, Category, Comment
# Register your models here.

admin.site.register(User)
admin.site.register(Listing_item)
admin.site.register(Comment)
admin.site.register(Category)
