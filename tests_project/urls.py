from django.urls import path

from tests_project import views

app_name = 'tests'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('all_tests/', views.AllTestsView.as_view(), name='all_tests'),
    path('<int:pk>/', views.TestView.as_view(), name='test'),
    path('<int:pk>/take/', views.TestTake.as_view(), name='test_question'),
    #path('completed_tests/', views., name='completed_tests'),
]