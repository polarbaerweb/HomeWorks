from django import forms
from .models import Listings, Comments


class CreateListings(forms.ModelForm):

    def __init__(self, username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["user"].initial = username

    class Meta:
        model = Listings
        fields = (
            "title",
            "description",
            "initialBids",
            "category",
            "image",
            "user",
        )


class LeaveComment(forms.ModelForm):

    def __init__(self, email: str = None, listing: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["email"].initial = email
        self.fields["listing"].initial = listing

    class Meta:
        model = Comments
        fields = (
            "listing",
            "email",
            "comment"
        )