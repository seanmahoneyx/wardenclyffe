from django.shortcuts import render
from django.http.response import HttpResponse

def item_view(request):
    return HttpResponse("simple view")