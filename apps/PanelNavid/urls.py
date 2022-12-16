from django.urls import path
from .views import *

app_name = 'panel'

urlpatterns = [
    path('loginpanel/',LoginView.as_view(),name='login'),
    path('dashbord/',DashbordView.as_view(),name='dashbord'),
    path('beat/add/',AddBeatView.as_view(),name='add-beat'),   
    path('beat/add/free/',AddFreeBeatView.as_view(),name='add-free'),   
    path('beat/add/sale/',AddSaleBeatView.as_view(),name='add-sale'),   
    path('beat/modify/<pk>/',ModifyBeatView.as_view(),name='modify-beat'),   
    path('beat/delete/<id>/',DeleteBeat.as_view(),name='delete-beat'),   
    path('category/add/',AddCategoryView.as_view(),name='add-category'),   
    path('category/delete/<id>/',DeleteCategory.as_view(),name='delete-category'),
    path('category/modify/<pk>/',ModifyCategoryView.as_view(),name='modify-category'),
    path('beat/list/',BeatListView.as_view(),name='list-beat'),   
    path('category/list/',CategoryListView.as_view(),name='list-category'),   
    path('send_email/',SendEmailView.as_view(),name='send-email'),   
    path('messages/',MessagesView.as_view(),name='messages'),   
    path('messages/<pk>/',MessageView.as_view(),name='message'),   
    path('settings/',SettingsView.as_view(),name='settings'),   
    path('settings/background/',ChangeBackground.as_view(),name='change-background'),   
    path('orders/',OrdersView.as_view(),name='orders'),   
]
