from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.http import HttpResponseRedirect
from . import util

class search(forms.Form):
    q = forms.CharField(max_length=100,
    widget=forms.TextInput(attrs={'class':'search', 
    "placeholder":"Search Encyclopedia"}), label="")

def index(request):
    if request.method == "POST":
        # Getting the data from the form
        form = search(request.POST)
        if form.is_valid():
            # Getting the query from the user
            q = form.cleaned_data['q']

            # Appending any entry that matches the query to a list
            results = []
            for entry in util.list_entries():
                if q in entry:
                    results.append(entry)

            # Returning that list to the user
            return render(request, "encyclopedia/results.html",{
                "results":results
            })
            pass
        else:
            return render(request, "encyclopedia/error.html",{
                pass
            })
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form":search()
    })

def wiki(request, TITLE):
    return render(request, "encyclopedia/wiki.html", {
        "TITLE":TITLE,
        "content":util.get_entry(TITLE)
    })

