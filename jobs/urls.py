from django.contrib import admin
from django.urls import path
from jobs import views

urlpatterns = [
    path("",views.index,name='jobs'),
    path("dashboard/",views.dashboard,name='dashboard'),
    path("login/", views.loginpage, name='login'),
    path("register/", views.register, name='register'),
    path("addjob/<str:pk>", views.addjob, name='addjob'),
    path("jobpage/<str:pk>", views.jobpage, name='jobpage'),
    path("solve/<str:pk>", views.solve, name='solve'),
    path("modal/", views.modalform, name="modalform"),
    path("interviews/",views.interviews,name='interviews'),
]
