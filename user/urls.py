from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.UserLogin.login, name='login'),
    path('logout/', views.UserLogin.logout, name='logout'),
    path('profile/', views.UserLogin.profile, name='update or create'),
    path('updating_profile_picture/', views.UserLogin.updating_profile_picture, name='updating profile picture'),
    path('updating_profile_to_super_user/', views.UserLogin.updating_profile_to_super_user, name='updating_porfile_to_super_user'),
]