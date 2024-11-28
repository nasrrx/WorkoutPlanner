from django.urls import path
from frontend import views
urlpatterns = [
    path('',views.index,name='index'),
    path('SignUp',views.SignUp,name='SignUp'),
    path('Home',views.Home,name='Home'),
    path('Profile',views.Profile,name='Profile')
]
