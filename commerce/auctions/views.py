import termios
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Category, Listing_item, Comment


def index(request):
    active_listing_items = Listing_item.objects.exclude(isActive=False).all()
    return render(request, "auctions/index.html", {
        "listing_items": active_listing_items
    })

@login_required
def createListing(request):
    if request.method == "POST":
        title = request.POST['name']
        desc = request.POST['description']
        price = request.POST['starting_bid']
        url = request.POST['picture']
        category = request.POST['category']
        user = request.user
        createListing = Listing_item(
            title = title,
            description = desc,
            starting_bid = float(price),
            category = category,
            owner = user
        )
        createListing.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        categories = Category.objects.all()
        return render(request, "auctions/create.html", {
            "categories": categories
        })

def addWatchlist(request, listing_id):
    if request.method == "POST":
        listing = Listing_item.objects.get(listing_id)
        user = request.user
        listing.watchlist.add(user)
        return HttpResponseRedirect(reverse("listing.html", args=(listing.id, )))

def listing(request, listing_id):
    listing = Listing_item.objects.get(pk = listing_id)
    comments = Comment.objects.filter(listing_item_id = listing_id)
    owner = listing.owner
    return render(request, "auctions/listing.html", {
        "listing_item": listing,
        "comments": comments,
        "owner": owner
    })

@login_required
def sell(request, listing_id):
    if request.method == "POST":
        listing = Listing_item.objects.get(pk = listing_id)
        listing.isActive = False
        return HttpResponseRedirect(reverse("index.html"))

def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category(request, category_id):
    category = Category.objects.get(pk = category_id)
    listings = Listing_item.objects.filter(category = category)
    return render(request, "auctions/category.html", {
        "listings": listings
    })


@login_required
def commenting(request, listing_id):
    if request.method == "POST":
        listing_item = listing_items.objects.get(pk=listing_id)
        comment = request.POST['comment']
        comment.comments.add(listing_item)
        return  HttpResponseRedirect(reverse("listing"), args=(listing_item.id,))

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
