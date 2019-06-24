# from django.http import HttpResponse
from django.shortcuts import render




def home_page(request):
    txt = 'Hello from Render !!!'
    context = {
    'txt': txt
    }
    return render(request, 'home.html', context)
