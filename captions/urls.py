from django.urls import path
from . import views

urlpatterns = [
    path('', views.caption_page,name="caption_page"),
    path("ideas/", views.ideas_list_partial, name="ideas-list-partial"),
    path("use-idea/<int:idea_id>/", views.use_idea, name="use-idea"),
    path('generate-captions/',views.generate_caption,name='generate_captions'),
    path("set-style/", views.set_caption_style, name="set_caption_style"),
]