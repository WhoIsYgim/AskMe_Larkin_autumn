from django.urls import path
from app import views


urlpatterns = [
    path('', views.index, name="index"),
    path('questions/', views.index, name='questions'),
    path('questions/hot/', views.index, name='hot'),
    path('questions/recent/', views.recent, name='recent'),
    path('questions/<int:i>/', views.question, name="single_q"),
    path('ask/', views.ask, name="askform"),
    path('login/', views.login_view, name="login_page"),
    path('logut', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
    path('tag/<str:title>/', views.tag, name="single_tag"),
    path('profile/<int:i>/', views.profile, name="profile"),
    path('profile/edit/', views.profile_edit, name="profile_edit")
]

