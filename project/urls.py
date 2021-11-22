from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path, include

from tests_project.views import SignUpView, LoginView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tests_project.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
