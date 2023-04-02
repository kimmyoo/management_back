from django.urls import path, include
from apps.classes import views

urlpatterns = [
    path('classes/', views.AllClassesList.as_view()),
    path('class/detail/<int:pk>', views.ClassDetail.as_view()),
    path('classes/in/program/<int:pk>/', views.ClassesInProgramList.as_view()),
    path('classes/takenby/student/<int:pk>/', views.ClassesTakenByStudent.as_view()),
    
    path('students/', views.AllStudentsList.as_view()),
    path('student/detail/<int:pk>', views.StudentDetail.as_view()), 
    path('students/in/class/<int:pk>/', views.StudentsInClassList.as_view()),   
]
