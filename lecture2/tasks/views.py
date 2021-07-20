from django.shortcuts import render
from django import forms

class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")
    priority = forms.IntegerField(label="Priority", min_value=1, max_value=8)

tasks = ['foo', 'bar', 'baz']
# Create your views here.
def index(request):
    return render(request, "tasks/index.html", {
        "tasks":tasks
    })

def add(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            # getting the task variable from the cleaned form
            task = form.cleaned_data['task']

            # Appening the task to the list of task
            tasks.append(task)

            # Redirect user to the list of task 
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