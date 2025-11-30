from django.urls import path
from .views import *
urlpatterns = [
    path('dashboard/', dashboard,name='dashboard' ),
    path('ideas/', idea_list,name='idea_list'),
    path('', landing_page,name='landing_page'),
]
