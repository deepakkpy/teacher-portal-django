
from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home, name='home'),
    # APIs
    path('api/students/', views.api_students, name='api_students'),
    path('api/students/add/', views.api_student_add, name='api_student_add'),
    path('api/students/<int:pk>/update/', views.api_student_update, name='api_student_update'),
    path('api/students/<int:pk>/delete/', views.api_student_delete, name='api_student_delete'),
]
