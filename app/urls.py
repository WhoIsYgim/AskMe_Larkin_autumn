from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name="index"),
    path('ask/', views.ask, name="askform"),
    path('login/', views.login, name="login_page"),
    path('register/', views.register, name="register"),
    path('questions/<int:i>/', views.question, name="single_q"),
    path('questions/<int:i>/answer/<int:j>', views.answer, name="single_ans"),

    path('profile/<int:i>/', views.profile, name="profile"),
]