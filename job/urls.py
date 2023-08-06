from django.urls import path
from . import views

urlpatterns = [
     path('', views.landing_page, name='landing_page'),
    path('list', views.job_application_list, name='job_application_list'),
    path('job_application/<int:pk>/', views.job_application_detail, name='job_application_detail'),
    path('job_application/create/', views.job_application_create, name='job_application_create'),
    path('job_application/update/<int:pk>/', views.job_application_update, name='job_application_update'),
    path('job_application/delete/<int:pk>/', views.job_application_delete, name='job_application_delete'),
    path('job_application/download/<int:pk>/', views.download_email, name='download_email'),
    path('thankyou/', views.thankyou, name='thankyou'),

]
