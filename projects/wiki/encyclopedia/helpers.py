from django import forms
from django.http import HttpResponseRedirect
from . import util
from django.shortcuts import render
from django.template.defaultfilters import stringfilter
from markdown2 import Markdown

class search(forms.Form):
    q = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class':'search', 
            "placeholder":"Search Encyclopedia"
        }), label="")

class createPage(forms.Form):
    title = forms.CharField(label="",
        required=True,    
        widget=forms.TextInput(attrs={
            "class":"form-control form-control-lg",
            "placeholder":"Title",
        }))

    content = forms.CharField(label="",
        required=True,    
        widget=forms.Textarea(attrs={
            "rows":"10", 
            "cols":"10",
            "class":"form-control form-control-lg",
            "placeholder":"Markdown Content"
        }))

class editPage(forms.Form):
    title = forms.CharField(label="Title",disabled = False,required = False,
    widget= forms.TextInput(attrs={
       'class':'col-md-12',
       "style":"margin:5px"
        }))
   
    content = forms.CharField(label="Markdown Content", 
    #help_text="<p class='text-secondary'>Please refer <a class='text-info' href = https://docs.github.com/en/github/writing-on-github/basic-writing-and-formatting-syntax> GitHub’s Markdown guide</a> </p>",
    widget= forms.Textarea(attrs={
    "rows":"10", 
    "cols":"10",
    'class':"form-control form-control-lg",
    'style':"top:2rem; margin:5px"
    }))

def get_page(request, TITLE):
    # If page found returning page
    markdowner = Markdown()

    html_wiki_page = markdowner.convert(util.get_entry(TITLE.lower()))
    if  util.get_entry(TITLE.lower()):
        return render(request, "encyclopedia/wiki.html",{
            "TITLE":TITLE.capitalize(),
            "form":search(),
            "content":html_wiki_page
        })
    # Else returning error
    return render(request, "encyclopedia/error.html", {
        "form":search
    })