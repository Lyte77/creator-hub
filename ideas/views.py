from django.shortcuts import render,get_object_or_404 
from django.contrib.auth.decorators import login_required
from django.db import transaction
from .models import Idea
from django.http import HttpResponse, JsonResponse,HttpResponseBadRequest
from planner.models import ContentTask
from django.views.decorators.http import require_POST

# Create your views here.


def landing_page(request):
    return render(request,'ideas/landing.html')


   


def dashboard(request):
     return render(request,'app_shell.html')
   
def idea_page(request):
    recent_ideas = Idea.objects.filter(user=request.user).order_by('-created_at')[:5]
    context ={
        'recent_ideas':recent_ideas
    }
    if request.headers.get("HX-Request"):
        return render(request, "ideas/partials/idea_page.html", context)

    # return render(request, "ideas/partials/idea_page.html", context)
   



def idea_list(request):
    ideas = Idea.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'ideas':ideas
    }
    return render(request,'ideas/idea_list.html',context)

# def add_idea(request):
#     if request.method == "POST":
#         content = request.POST.get("content")
#         idea = Idea.objects.create(user=request.user, content=content)

#         ContentTask.objects.create(
#             user=request.user,
#             title=content[:60],
#             idea=idea,
#             status="draft"
#         )
#         return render(request, "ideas/partials/idea_item.html", {"idea": idea})


@login_required
@require_POST
def add_idea(request):
    content = request.POST.get("content", "").strip()

    # Guard clause: empty input
    if not content:
        if request.headers.get("HX-Request"):
            return render(
                request,
                "ideas/partials/idea_error.html",
                {"error": "Idea cannot be empty"},
                status=400
            )
        return HttpResponseBadRequest("Invalid input")

    try:
        with transaction.atomic():
            idea = Idea.objects.create(
                user=request.user,
                content=content
            )

            # Optional: auto-create draft task
            ContentTask.objects.create(
                user=request.user,
                idea=idea,
                title=content[:60],
                status="draft"
            )

    except Exception:
        if request.headers.get("HX-Request"):
            return render(
                request,
                "ideas/partials/idea_error.html",
                {"error": "Something went wrong. Try again."},
                status=500
            )
        raise

    return render(
        request,
        "ideas/partials/idea_item.html",
        {"idea": idea}
    )
    
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

    remaining_count = Idea.objects.filter(user=request.user).count()
    
    # If it was the last one, return the OOB "No Ideas" partial
    if remaining_count == 0:
        return render(request, "ideas/partials/last_idea_deleted.html")
    return HttpResponse('')


def idea_item(request, pk):
    idea = get_object_or_404(Idea, id=pk, user=request.user)
    return render(request, "ideas/partials/idea_item.html", {"idea": idea})
