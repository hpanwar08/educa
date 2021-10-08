from django.urls import path

from courses.api import views

app_name = 'courses_api'

urlpatterns = [
    path('subjects/', views.SubjectListView.as_view(), name='subject_list'),
    path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('courses/<pk>/enroll/', views.CourseEnrollView.as_view(), name='course_enroll')
]
