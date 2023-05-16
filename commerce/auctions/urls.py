from django.urls import path
from django.conf.urls.static import static
from commerces import settings

from . import views

urlpatterns = [
    path("", views.ListingsList.as_view(), name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create-listings/", views.create_listings, name="create-listings"),
    path("detail/<auctionObject>/", views.get_details, name="detail"),
    path("detail/<auctionObject>/make-bid/", views.make_bid, name="make-bid"),
    path("detail/<auctionObject>/add-comment/", views.add_comment, name="add-comment"),
    path("detail/<auctionObject>/remove-comment/", views.remove_comment, name="remove-comment"),
    path("watchlist/", views.get_watchlist, name="watchlist"),
    path("watchlist/add/<int:item_id>/", views.add_to_watchlist, name='add_to_watchlist'),
    path("watchlist/remove_from_watchList/<int:item_id>/", views.remove_from_watchlist, name='remove_from_watchList'),
    path("delete/<int:itemId>", views.close_auction, name="close-auction"),
    path("categories/", views.category_list, name="categories"),
    path("categories/<category>", views.get_by_category, name="category")
]

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
