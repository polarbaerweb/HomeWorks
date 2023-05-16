from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView
from django.core.exceptions import ObjectDoesNotExist

from .models import (User,
                     Listings,
                     WatchList,
                     Comments,
                     Bid)

from .form import CreateListings, LeaveComment

MAIN_PAGE = "auctions/index.html"
CREATE_LISTINGS_PAGE = "auctions/add.html"
DETAIL_LISTING_PAGE = "auctions/detail.html"


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


class ListingsList(ListView):
    queryset = Listings.objects.filter(winner__isnull=True).order_by("title")
    model = Listings
    context_object_name = "listings"
    template_name = "listings_list.html"


def category_list(request):
    types = [{"LA": "LiveAuction"}, {"OA": "OnlineAuction"}, {"SBA": "SealedBidAuction"}]

    return render(request, "auctions/categories.html", {
        "types": types
    })


def get_by_category(request, category: str):
    listingsByAuctionCategory = Listings.objects.filter(category=category, winner__isnull=True).order_by("title")
    isThereAuction = True if Listings.objects.exists() and not listingsByAuctionCategory else False


    return render(request, "auctions/listings_list.html", {
        "listings": listingsByAuctionCategory,
        "isThereAuction": isThereAuction
    })


@login_required
def create_listings(request):
    if request.method == "POST":
        createListingForm = CreateListings(username=request.user.username, data=request.POST, files=request.FILES)

        if createListingForm.is_valid():
            createListingForm.save()
            return HttpResponseRedirect(".")
        else:
            return HttpResponseRedirect("/")

    else:
        createListingForm = CreateListings(username=request.user.username)

    return render(request, CREATE_LISTINGS_PAGE, {"form": createListingForm})


def get_details(request, auctionObject: str):
    try:
        listing = Listings.objects.get(title=auctionObject)
        bids = listing.bids.filter(listing=listing).first()
        comments = Comments.objects.filter(listing=listing)
        userEmail = request.user.email
        listingTitle = listing.title

        print(comments)

    except ObjectDoesNotExist:
        message = "Could not find a bid for this element"
        return render(request, "auctions/message.html", {
            "message": message
        })

    except IndexError:
        return HttpResponseRedirect("/")

    else:
        return render(request, DETAIL_LISTING_PAGE, {"content": listing,
                                                     "bids": bids or "it was by default",
                                                     "form": LeaveComment(email=userEmail, listing=listingTitle),
                                                     "comments": comments
                                                     })


@login_required
def add_comment(request, auctionObject: str):
    if request.method == "POST":
        listing = Listings.objects.get(title=request.POST["listing"])
        email = User.objects.get(email=request.POST["email"])
        comment = request.POST["comment"]

        db = Comments(listing=listing, email=email, comment=comment)
        db.save()

        return HttpResponseRedirect("..")

    return HttpResponseRedirect("..")


# !TODO
@login_required
def remove_comment(request, auctionObject: str):
    pass


@login_required
def add_to_watchlist(request, item_id: int):
    item = get_object_or_404(Listings, id=item_id)
    watchlist, created = WatchList.objects.get_or_create(user=request.user)
    watchlist.title.add(item)

    return HttpResponseRedirect("/watchlist/")


@login_required
def remove_from_watchlist(request, item_id: int):
    title = get_object_or_404(Listings, id=item_id)
    watchlist = get_object_or_404(WatchList, user=request.user)
    watchlist.title.remove(title)
    return HttpResponseRedirect('/')


@login_required
def get_watchlist(request):
    try:
        watchlist = WatchList.objects.get(user=request.user)
        listings = watchlist.title.filter(winner__isnull=True)
        return render(request, 'auctions/watchlist.html', {"listings": listings})
    except ObjectDoesNotExist:
        return render(request, 'auctions/watchlist.html', {"message": "You do not have any item in your watchlist"})


@login_required
def make_bid(request, auctionObject: str):
    listing = get_object_or_404(Listings, title=auctionObject)
    errorBidMessage = "Sorry yor bid must be highest"
    errorValueMessage = "Invalid Value"

    if request.method == "POST":
        bidAmount = request.POST["bidAmount"]

        if bidAmount:
            try:
                bidAmount = float(bidAmount)
            except ValueError:
                return render(request, "auctions/message.html", {
                    "message": errorValueMessage
                })
            else:
                if bidAmount >= listing.initialBids:
                    highestBid = listing.bids.order_by("-amount").first()  # get the highest bid
                    highestBid = highestBid is not None and highestBid.amount

                    if not highestBid or bidAmount > highestBid:
                        listing.initialBids = bidAmount  # update the initialBids in Listings

                        try:
                            _bid = Bid.objects.get(listing=listing)
                            _bid.user = request.user
                            _bid.amount = bidAmount
                        except ObjectDoesNotExist:
                            _bid = Bid(listing=listing, user=request.user, amount=bidAmount)
                        finally:
                            _bid.save()
                            listing.save()  # save a new bid

                        return HttpResponseRedirect("..")
                    else:

                        return render(request, "auctions/message.html",
                                      {"message": errorBidMessage})
                else:
                    return render(request, "auctions/message.html", {"message": errorBidMessage})

        else:
            return HttpResponseRedirect("/")


@login_required
def close_auction(request, itemId: int):
    auctionItem = Listings.objects.get(id=itemId)

    if request.user == auctionItem.user:
        auctionItem.active = False

        highestBid = auctionItem.bids.order_by("-amount").first()

        if highestBid:
            auctionItem.winner = highestBid.user
            auctionItem.save()
            message = f"The winner is {auctionItem.winner}"
        else:
            message = "The error occurred no bids found"

        return render(request, "auctions/message.html", {"message": message})

    return render(request, "auctions/message.html", {"message": f"The owner is {auctionItem.user}"})
