from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("donors_list/<int:myid>/", views.donors_list, name="donors_list"),
    path("donors_details/<int:myid>/", views.donors_details, name="donors_details"),
    path("request_fund/", views.request_fund, name="request_fund"),
    path("see_all_request/", views.see_all_request, name="see_all_request"),
    path("become_donor/", views.become_donor, name="become_donor"),
    path("donation_list/", views.Donation_list, name="donation_list"),
    path("make_donation/", views.make_donation, name="make_donation"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('change_status/', views.change_status, name='change_status'),
    path('see_all_donations/', views.see_all_donations, name='see_all_donations'),
    path("forgotpwd/", views.forgotpwd, name="forgotpwd"),
    path("reset_password/<str:username>", views.reset_password, name="reset_password"),
]