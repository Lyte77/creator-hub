

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/",include("allauth.urls")),
    path('user/',include('users.urls')),
    path('',include('ideas.urls')),
    path('captions/',include('captions.urls')),
    path('planner/',include('planner.urls')),

]
