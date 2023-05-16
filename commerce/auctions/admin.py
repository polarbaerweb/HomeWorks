from django.contrib import admin

from . import models


class CreateListingsSetting(admin.ModelAdmin):
    list_display = (
        "title",
        "initialBids",
        "winner"
    )


class UserSetting(admin.ModelAdmin):
    list_display = (
        "email",

    )


class CommentsSettings(admin.ModelAdmin):
    list_display = (
        "email",
    )


class WatchListSettings(admin.ModelAdmin):
    list_display = (
        "user",
    )


class BidsSettings(admin.ModelAdmin):
    list_display = (
        "listing",
        "amount"
    )


admin.site.register(models.Listings, CreateListingsSetting)
admin.site.register(models.User, UserSetting)
admin.site.register(models.Comments, CommentsSettings)
admin.site.register(models.WatchList, WatchListSettings)
admin.site.register(models.Bid, BidsSettings)
