from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.http import HttpResponseRedirect
from . import util

class search(forms.Form):
    q = forms.CharField(max_length=100,
    widget=forms.TextInput(attrs={
        'class':'search', 
        "placeholder":"Search Encyclopedia"
    }), label="")

class createPage(forms.Form):
    title = forms.CharField(label="",
    required=True,    
    widget=forms.TextInput(attrs={
        "class":"form-control form-control-lg",
        "placeholder":"Title"
    }))

    markdown = forms.CharField(label="",
    required=True,
    widget=forms.Textarea(attrs={
        "class":"form-control form-control-lg",
        "placeholder":"Enter your Markdown Content"
    }))

def index(request):
    if request.method == "POST":
        # Getting the data from the form
        form = search(request.POST)

        if form.is_valid():
            # Getting the query from the user
            q = form.cleaned_data['q'].lower()

            # if the entry is in our files, the display entry
            if util.get_entry(q):
                return render(request, "encyclopedia/wiki.html",{
                    "TITLE":q,
                    "content":util.get_entry(q),
                    "form":search()
                })

            # Else searching if q is substring of entry
            results = []
            for entry in util.list_entries():
                if q.lower() in entry.lower():
                    results.append(entry)

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
    return render(request, "encyclopedia/wiki.html", {
        "TITLE":TITLE.capitalize(),
        "content":util.get_entry(TITLE.lower()),
        "form":search()
    })

def newPage(request):
    # Checking the request method
    if request.method == "POST":
        form = createPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["markdown"]

            util.save_entry(title, content)
            return render(request, "encyclopedia/wiki.html",{
                    "TITLE":title,
                    "content":content,
                    "form":search()
                })
        # There form was not valid
        return render(request, "encyclopedia/error.html")
    
    # GET request
    return render(request, "encyclopedia/newPage.html", {
        "form":search(),
        "newPage":createPage()
    })

