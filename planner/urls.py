from django.urls import path
from . import views

urlpatterns = [
    # path('',views.planner_page,name='planner_page'),
    path('',views.planner_page2,name='planner_page'),
    path('plan-week',views.planner_week,name='planner_week'),
    path('drafts/',views.planner_drafts,name='planner_drafts'),
    path('task/<int:task_id>/schedule/',views.schedule_task,name='schedule_task'),
    path('task/<int:task_id>/unschedule/',views.unschedule_task,name='unschedule_task'),
]

