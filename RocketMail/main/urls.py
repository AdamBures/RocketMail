from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('profile/<str:username>/', views.my_view, name='profile'),
    path('send', views.send_email, name='send'),
    path('emails', views.get_emails, name="emails")
]
