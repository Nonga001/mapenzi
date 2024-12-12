from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Homepage path
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),  # Login path
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Logout path
    path('profile/', views.profile, name='profile'),  # Profile page
    path('enrollment/', views.enrollment, name='enrollment'),  # Enrollment page
    path('course/', views.course, name='course'),  # Course page
    path('create-announcement/', views.create_announcement, name='create_announcement'),  # Create Announcement path
    path('announcement/edit/<int:id>/', views.edit_announcement, name='edit_announcement'),  # Edit Announcement path
    path('announcement/delete/<int:id>/', views.delete_announcement, name='delete_announcement'),  # Delete Announcement path
]
