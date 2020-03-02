from django.urls import path, include
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name="dashboard"),
    path('starting/', views.starting, name="starting"),
    path('', views.signup, name="signup"),
    path('login/', views.login, name="login"),
    path('register/', views.register, name="register"),
    path('do_login/', views.do_login, name="do_login"),
    path('tasks/', views.tasks, name='tasks'),
    path('task_done', views.task_done, name='task_done'),
    path('all_members', views.all_members, name="all_members"),
    path('members', views.members, name="members"),
    path('logout', views.logout, name="logout"),
    path('chat', views.chat, name="chat"),
    path('discussion', views.discussion, name="discussion"),
    path('chatting', views.chatting, name="chatting")

]

