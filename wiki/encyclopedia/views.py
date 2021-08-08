from django.shortcuts import render
from django.urls import reverse
from . import util
from .helpers import *
from random import choice
from markdown2 import Markdown

def index(request):
    if request.method == "POST":
        # Getting the data from the form
        form = search(request.POST)

        if form.is_valid():
            # Getting the query from the user
            q = form.cleaned_data['q'].lower()

            # if the entry is in our files, the display entry
            if util.get_entry(q.replace(" ", "_")):
                return render(request, "encyclopedia/wiki.html",{
                    "TITLE":q,
                    "content":util.get_entry(q),
                    "form":search()
                })

            # Else searching if q is substring of entry
            results = []
            for entry in util.list_entries():
                if q.lower() in entry.lower():
                    results.append(entry.replace("_", " "))

            return render(request, "encyclopedia/results.html",{
                "results":results,
                "form":search()
            })

        # Form is not valid
        return render(request, "encyclopedia/error.html", {
            "form":search()
        })
    
    # Get Request
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":search()
    })

def wiki(request, TITLE):
    return get_page(request, TITLE)
    
def newPage(request):
    # Checking the request method
    if request.method == "POST":
        form = createPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["markdown"]

            util.save_entry(title.lower().replace(" ", "_"), content)
            return get_page(title.lower())
        # There form was not valid
        return render(request, "encyclopedia/error.html")
    
    # GET request
    return render(request, "encyclopedia/newPage.html", {
        "form":search(),
        "newPage":createPage()
    })

def edit(request):
    # Getting the form by its id 
    title = request.POST.get("edit")

    content = util.get_entry(title.lower())
    
    # def fun():
    #     return editPage(title, content)

    # edit_form = forms.EditPageForm(initial={
    #     'pagename': title, 
    #     'body':content
    #     })
    return render(request, "encyclopedia/editPage.html", {
        "TITLE":title.capitalize(),
        "form":search(),
        "editForm":editPage(initial={'title': title, 'content':content})
    })

def save(request):
    form = editPage(request.POST)

    if form.is_valid(): 
        title = form.cleaned_data["title"]
        content = form.cleaned_data["content"]

        util.save_entry(title, content)

        return get_page(request, title)
    return(request, "encyclopedia/editPage.html", {
        "form":search(),
        "editForm":form
    })

def randomPage(request):
    return get_page(request, choice(util.list_entries()) )

