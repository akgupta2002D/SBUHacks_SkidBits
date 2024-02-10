from django.shortcuts import render, redirect

# Create your views here.


def homepage(request):
    return render(request, "mainpage/base.html")


def record_page(request):
    return render(request, "mainpage/record.html")
