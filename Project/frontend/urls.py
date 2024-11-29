from django.urls import path
from frontend import views
urlpatterns = [
    path('',views.login_view,name='LogIn'),
    path('SignUp',views.signup_view,name='SignUp'),
    path('Home',views.Home,name='Home'),
    path('Profile',views.Profile,name='Profile')
]
