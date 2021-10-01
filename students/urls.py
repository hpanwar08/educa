from django.urls import path

from students import views

app_name = 'students'

urlpatterns = [
    path('register/', views.StudentRegistrationView.as_view(), name='student_registration'),
]
