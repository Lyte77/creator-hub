from django.urls import path
from .views import *
urlpatterns = [
    path('dashboard/', dashboard,name='dashboard' ),
    path('ideas/', idea_list,name='idea_list'),
    path('', landing_page,name='landing_page'),
    path('add_idea/', add_idea,name='add_idea'),
    path('edit_idea/<int:pk>/', edit_idea,name='edit_idea'),
    path('idea_item/<int:pk>/', idea_item,name='idea_item'),
    path('delete_idea/<int:pk>/', delete_idea,name='delete_idea'),
]
