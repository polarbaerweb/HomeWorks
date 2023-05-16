from django import forms

DEFAULT_INITIAL_LABEL_TITLE = "Title"
DEFAULT_INITIAL_LABEL_ARTICLE = "Article"


class AddNewArticle(forms.Form):
    title = forms.CharField(max_length=255)
    article = forms.CharField(widget=forms.Textarea())

    def __init__(self, title: str = DEFAULT_INITIAL_LABEL_TITLE,
                 article: str = DEFAULT_INITIAL_LABEL_ARTICLE,
                 *args,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].initial = title
        self.fields["article"].initial = article
