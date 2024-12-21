from django.urls import path
from LiftRight import views

urlpatterns = [
    path('',views.RenderLoginView,name='LogIn'),
    path('SignUp',views.RenderSignUpView,name='SignUp'),
    path('Home',views.RenderHomePage,name='Home'),
    path('Profile',views.LoadProfileUserData,name='Profile'),
    path('About',views.RenderAboutPage,name='About'),
    path('download/', views.download_workout_plan, name='download_workout_plan'),
    path('update-profile/', views.update_profile, name='update_profile'),
    # path('api/gyms', views.get_nearby_gyms, name='get_nearby_gyms'),
    # path('Gyms', views.find_gyms, name='FindGyms'),
]
