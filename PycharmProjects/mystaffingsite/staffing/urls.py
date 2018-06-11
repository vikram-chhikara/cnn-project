from django.urls import path
from . import views

app_name = 'staffing'

urlpatterns =[
    path('', views.landing, name= 'landing'),
    path('clientSignupOrLogin/', views.clientSignupOrLogin, name= 'clientSignupOrLogin'),
    path('applicantSignupOrLogin/', views.applicantSignupOrLogin, name= 'applicantSignupOrLogin'),
    path('managerLogin/', views.managerLogin, name= 'managerLogin'),
    path('recruiterLogin/', views.recruiterLogin, name= 'recruiterLogin'),
    path('applicantDashboard/<int:applicant_id>/', views.applicantDashboard, name= 'applicantDashboard'),
    path('clientDashboard/<int:client_id>/', views.clientDashboard, name= 'clientDashboard'),
    path('clientDashboard/<int:client_id>/newPosting/', views.newPosting, name= 'newPosting'),
    path('recruiterDashboard/<int:recruiter_id>/', views.recruiterDashboard, name= 'recruiterDashboard'),
    path('recruiterDashboard/<int:recruiter_id>/searchJobPosting/', views.searchJobPosting, name= 'searchJobPosting'),
    path('recruiterDashboard/<int:recruiter_id>/searchApplicant/', views.searchApplicant, name= 'searchApplicant'),
    path('managerDashboard/<int:manager_id>/', views.managerDashboard, name= 'managerDashboard'),
    path('managerDashboard/<int:manager_id>/newRecruiter/', views.newRecruiter, name= 'newRecruiter'),
    path('managerDashboard/<int:manager_id>/editRecruiter/<int:recruiter_id>/', views.editRecruiter, name='editRecruiter'),
    path('managerDashboard/removeRecruiter/<int:recruiter_id>/', views.removeRecruiter, name='removeRecruiter'),
    path('logoutView/', views.logoutView, name = 'logoutView'),
]