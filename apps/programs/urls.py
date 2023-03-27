from django.urls import path, include
# here remember to add apps.
from apps.programs import views

urlpatterns = [
    path('programs/', views.allProgramsList.as_view()),
    path('programs/detail/<int:pk>', views.ProgramDetail.as_view()),
]
