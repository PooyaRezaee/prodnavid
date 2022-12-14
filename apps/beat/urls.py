from django.urls import path
from .views import *

app_name = 'beat'

urlpatterns = [
    path('',HomeView.as_view(),name='index'),
    path('beat/<int:code_beat>/',DetailBeatView.as_view(),name='detail'),
    path('beats/',ListBeatView.as_view(),name='list'),
    path('beats/free/',FreeListBeatView.as_view(),name='free'),
    path('beats/free/<slug:category_slug>/',FreeListBeatView.as_view(),name='category-free'),
    path('beats/<slug:category_slug>/',ListBeatView.as_view(),name='category'),
    path('developer/',DeveloperView.as_view(),name='developer'),
    path('aboutme/',AboutView.as_view(),name='about'),
]
