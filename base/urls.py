from django.urls import path 
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerPage, name='register'),
    path('', views.home, name="home"),
    path('user_profile/<str:id>', views.user_profile, name='user-profile'),
    path('room/<str:id>', views.room, name="room"),
    path('create_room/', views.create_room, name="create-room"),
    path('update_room/<str:id>', views.update_room, name='update-room'),
    path('delete_room/<str:id>', views.delete_room, name='delete-room'),
    path('delete_message/<str:id>', views.delete_message, name='delete-message'),
]