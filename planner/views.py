from django.shortcuts import render,get_object_or_404
from .models import ContentTask
from ideas.models import Idea
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.

def planner_week(request):
    week_offset = int(request.GET.get("week", 0))

    today = date.today()
    reference_date = today + timedelta(weeks=week_offset)

    week_start, week_end = get_week_bounds(reference_date)

    # Build list of days
    days = [(week_start + timedelta(days=i)) for i in range(7)]

    # Pull tasks for the entire week (single DB hit)
    tasks = ContentTask.objects.filter(
        user=request.user, scheduled_date__range=[week_start, week_end]
    ).order_by("scheduled_date")

    # Group tasks by each day
    day_map = {d: [] for d in days}
    for t in tasks:
        day_map[t.scheduled_date].append(t)

    # Prepare context in template-friendly structure
    week_days = [(day, day_map.get(day, [])) for day in days]




    context = {
        "week_start": week_start,
        "week_end": week_end,
        "week_days": week_days,
        "prev_week": week_offset - 1,
        "next_week": week_offset + 1,
        
    }

    return render(request, "partials/_week.html", context)



def planner_page2(request):
    return render(request, "planner/planner_page.html")


def planner_drafts(request):
    draft_tasks  = ContentTask.objects.filter(
        user=request.user,
        scheduled_date__isnull=True,
        status="draft"
    ).order_by("-created_at")
    if draft_tasks:
        for i in draft_tasks:
            print(i.title)
    else:
        print("no drafts")

    return render(
        request,
        "partials/_draft_list.html",
        {"draft_tasks": draft_tasks}
    )


def get_week_bounds(reference_date):
    """Returns Monday and Sunday of the week for a given date."""
    monday = reference_date - timedelta(days=reference_date.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday







def schedule_task(request, task_id):
    task = get_object_or_404(ContentTask, id=task_id, user=request.user)

    
    

    if request.method == "POST":
        date_str = request.POST.get("scheduled_date")
        platform = request.POST.get("platform")

        task.scheduled_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        task.platform = platform
        task.status = "planned"
        task.save()

        target_id = f"day-{request.POST.get('scheduled_date')}"
        # return updated planner fragment
        return render(request, "partials/task_card.html", {
            "task": task,
            "target_day_id": target_id,
            
        })
   

    return render(request, "partials/task_modal.html", {
        "task": task,
        "today": date.today().strftime('%Y-%m-%d')
    })


def unschedule_task(request, task_id):
    task = get_object_or_404(ContentTask, id=task_id, user=request.user)
    task.scheduled_date = None
    task.status = 'draft'
    task.save()
    return render(request, "partials/oob_switch.html", {"task": task})