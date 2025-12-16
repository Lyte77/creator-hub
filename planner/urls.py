from django.urls import path
from . import views

urlpatterns = [
    path('',views.planner_page,name='planner_page'),
    path('task/create/',views.create_task,name='create_task'),
]

