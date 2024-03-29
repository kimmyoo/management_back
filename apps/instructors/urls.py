from django.urls import path, include
from apps.instructors import views

urlpatterns = [
    path('instructors/', views.AllInstructorsList.as_view()),
    path('licenses/', views.AllLicensesList.as_view()),
    path('licenses/<int:pk>', views.LicenseDetail.as_view()),
    # pk is instructor.id
    path('licenses/instructor/<int:pk>', views.InstructorLicenseList.as_view()),
    path('licenses/program/<int:pk>', views.ProgramLicenseList.as_view()),
    # pk is instructor.id
    path('instructors/detail/<int:pk>', views.InstructorDetail.as_view()),
]
