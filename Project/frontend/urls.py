from django.urls import path
from frontend import views
urlpatterns = [
    path('',views.login_view,name='LogIn'),
    path('SignUp',views.signup_view,name='SignUp'),
    path('Home',views.Home,name='Home'),
    path('Profile',views.Profile,name='Profile'),
    path('About',views.About,name='About'),
    path('download/', views.download_workout_plan, name='download_workout_plan'),
    path('update-profile/', views.update_profile, name='update_profile'),
]
