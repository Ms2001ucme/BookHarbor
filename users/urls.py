from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/',views.role_based_redirect,name='role_redirect'),
    path('dashboard/author/', views.author_dashboard, name='author_dashboard'),  
    path('dashboard/user/', views.user_dashboard, name='user_dashboard'),
    path("profile/", views.user_profile, name="user_profile"),
    path("profile/update/", views.profile_update, name="profile_update"),

    

]
