
from django.urls import path
from . import views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('save-week/', views.save_week, name='save_week'),
    path('internship-journal/', views.internship_journal, name='internship_journal'),
]
