from django.shortcuts import render,get_object_or_404 
from .models import Idea
from django.http import HttpResponse, JsonResponse

# Create your views here.


def landing_page(request):
    return render(request,'ideas/landing.html')

def dashboard(request):
   recent_ideas = Idea.objects.filter(user=request.user).order_by('-created_at')[:5]
   context ={
        'recent_ideas':recent_ideas
    }
   return render(request, 'ideas/dashboard.html',context)


def idea_list(request):
    ideas = Idea.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'ideas':ideas
    }
    return render(request,'ideas/idea_list.html',context)

def add_idea(request):
    if request.method == "POST":
        content = request.POST.get("content")
        idea = Idea.objects.create(user=request.user, content=content)
        return render(request, "ideas/partials/idea_item.html", {"idea": idea})

# def add_idea(request):
#     if request.method == "POST":
#         content = request.POST.get("content", "").strip()
#         if not content:
#             return JsonResponse({"error": "Idea cannot be empty"}, status=400)
        
#         idea = Idea.objects.create(user=request.user, content=content)
#         return render(request, "ideas/partials/idea_item.html", {"idea": idea})
    
#     return JsonResponse({"error": "Invalid request"}, status=400)
    
def edit_idea(request, pk):
    idea = get_object_or_404(Idea, pk=pk, user=request.user)

    if request.method == "POST":
        content = request.POST.get("content")
        idea.content = content
        idea.save()
        return render(request, "ideas/partials/idea_item.html", {"idea": idea})

    return render(request, "ideas/form.html", {"idea": idea})
    
def delete_idea(request, pk):
    idea = get_object_or_404(Idea, pk=pk, user=request.user)
    idea.delete()
    return HttpResponse('')


def idea_item(request, pk):
    idea = get_object_or_404(Idea, id=pk, user=request.user)
    return render(request, "ideas/partials/idea_item.html", {"idea": idea})
