from django.shortcuts import render
from .models import ContentTask
from ideas.models import Idea
from datetime import date, timedelta
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.

def planner_page(request):
     week_offset = int(request.GET.get("week", 0))

     today = date.today()
     reference_date = today + timedelta(weeks=week_offset)

     week_start, week_end = get_week_bounds(reference_date)

    # Build list of days
     days = [(week_start + timedelta(days=i)) for i in range(7)]

    # Pull tasks for the entire week (single DB hit)
     tasks = ContentTask.objects.filter(
        user=request.user,
        scheduled_date__range=[week_start, week_end]
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

     if request.headers.get("HX-Request"):
        return render(request, "partials/_week.html", context)
     return render(request,'planner/planner.html',context)


def get_week_bounds(reference_date):
    """Returns Monday and Sunday of the week for a given date."""
    monday = reference_date - timedelta(days=reference_date.weekday())
    sunday = monday + timedelta(days=6)
    return monday, sunday




@login_required
def create_task(request):
    if request.method == "POST":
        title = request.POST.get("title")
        scheduled_date = request.POST.get("scheduled_date")

        task = ContentTask.objects.create(
            user=request.user,
            title=title,
            scheduled_date=request.POST.get("scheduled_date"),
            platform=request.POST.get("platform") or None,
            status="planned"
        )

        # Return ONLY the new task card
        return render(request, "partials/task_card.html", {
            "task": task
        })

    # GET request → open modal
    date = request.GET.get("date")

    return render(request, "partials/task_modal.html", {
        "date": date
    })