


from site import venv
from unicodedata import name
from django.urls import include, path
from . import views

urlpatterns = [

    path('login',views.login,name='login'),
    path('',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('home',views.home,name='home'),
    path('saveuser',views.saveUser,name='saveuser'),
    path('isvaliduser',views.isvaliduser,name='isvaliduser'),
    path('forgot',views.forgot,name='forgot'),
    path('sendMail',views.sendMail,name='sendMail'),
]
