from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")

# Create your views here.
def index(request):
    # Creating tasks variable inside the session
    if "tasks" not in request.session:
        request.session['tasks'] = []
    return render(request, "tasks/index.html", {
        "tasks":request.session["tasks"]
    })

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            # getting the task variable from the cleaned form
            task = form.cleaned_data['task']

            # setting the value of the form to the session variable
            request.session['tasks'] += [task]
           
            # Redirect user to the list of task, uses name of page, not specific route
            # Reverse gets the name of a url, then returns the route 
            return HttpResponseRedirect(reverse("tasks:index"))
            
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "tasks/add.html", {
                # Returning any errors that may have occured
                "form":form
            })
    return render(request, "tasks/add.html",{
        "form": NewTaskForm()
    })