from django.http import Http404, HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "singlepage1/index.html")

texts = [
    "I guarentee that the Eagles are going to win their game this week against the 49ers",
    "I guarentee that the Chargers will beat the cowboys and Justin Herbert will throw for over 300 yards",
    "I guarentte that Kyler Murray and the Cardinals will dominate the Minnesota Vikings. Kyler Murray throws for over 290 yards, and scores 4 total touchdowns"
]

def section(request, num):
    if 1 <= num <= 3:
        return HttpResponse(texts[num - 1])
    else:
        return Http404("No such section")