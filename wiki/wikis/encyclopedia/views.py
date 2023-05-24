from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404

from . import util
from .form import AddNewArticle

MAIN_PAGE = "encyclopedia/index.html"
DETAIL_PAGE = "encyclopedia/detail.html"
MATCHED_PAGE = "encyclopedia/matched.html"
ADD_ARTICLE_PAGE = "encyclopedia/add.html"

BODY_MAIN_PAGE_TITLE = "All pages"
BODY_SEARCH_PAGE_TITLE = "Matched contents according to the query"

CREATE_MATCHED_ERROR_MESSAGE = "Please make sure that your title does not match with one of these"


def index(request):
    return render(request, MAIN_PAGE, {
        "entries": util.list_entries(),
        "bodyTitle": BODY_MAIN_PAGE_TITLE
    })


def getContent(request, contentName: str = None):
    content = util.get_entry(contentName)

    if content is None:
        raise Http404

    return render(request, DETAIL_PAGE, {"entries": content, "title": contentName, })


def search(request):
    read = request.GET.get("q")
    readeContent = util.get_entry(read)

    whichPage = DETAIL_PAGE

    def get_all_matched_contents():
        allContents = util.list_entries()
        contents_case = []

        """
            to figure out does one of the letter in read variable contains in content  
        """
        for content in allContents:
            for letter in read.lower():
                if letter in content.lower().strip():
                    contents_case.append(content)
                    break

        return contents_case

    if readeContent is None:
        whichPage = MAIN_PAGE

    return render(request, whichPage, {"entries": readeContent or get_all_matched_contents(), "bodyTitle": BODY_SEARCH_PAGE_TITLE})


def create_page(request):
    if request.method == "POST":
        title = request.POST.get("title").title()
        article = request.POST.get("article")

        allArticles = util.list_entries()

        if title in allArticles:
            return render(request, MAIN_PAGE, {"entries": allArticles, "bodyTitle": CREATE_MATCHED_ERROR_MESSAGE})

        util.save_entry(title, article)
        return redirect(reverse("detail", kwargs={"contentName": title}))

    return render(request, ADD_ARTICLE_PAGE, {"form": AddNewArticle, "typeUrl": "create-page"})


def edit_article(request, contentName: str = None):
    if request.method == "POST":
        title = request.POST.get("title").title()
        article = request.POST.get("article")

        util.save_entry(title, article)

        return redirect(reverse("detail", kwargs={"contentName": title}))

    content = util.get_entry(contentName)

    return render(request, ADD_ARTICLE_PAGE, {"form": AddNewArticle(title=contentName, article=content), "typeUrl": "edit-page"})
