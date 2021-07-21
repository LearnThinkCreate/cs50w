from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, TITLE):
    return render(request, "encyclopedia/wiki.html", {
        "TITLE":TITLE,
        "content":util.get_entry(TITLE)
    })

