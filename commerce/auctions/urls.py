from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>", views.commenting, name="commenting"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:listing_id>", views.addWatchlist, name="addWatchlist"),
    path("<int:listing_id>", views.sell, name="sell"),
    path("categories", views.categories, name="categories"),
    path("category/<int:category_id>", views.category, name="category"),
    path("create", views.createListing, name="create")
]
