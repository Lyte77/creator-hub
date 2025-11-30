from django.shortcuts import render

# Create your views here.


def landing_page(request):
    return render(request,'ideas/landing.html')

def dashboard(request):
    return render(request, 'ideas/dashboard.html')


def idea_list(request):
    return render(request,'ideas/idea_list.html')