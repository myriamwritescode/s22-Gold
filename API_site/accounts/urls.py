'''

urlpatterns - Contain all file path for this application

'''
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # <---- reset password

urlpatterns = [

    # ------------------------------------User Registration and Login Authentication-------------------
    path('register/', views.registerPage, name="register"),  # <----dynamic path
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    # ------------------------------------web page that display the information from the database---------
    path('', views.home, name="home"),
    path('profile/', views.userPage, name="user-page"),
    path('compare/', views.comparePage, name="user-compare"),
    path('value/', views.valuePage, name="user-value"),
   
    path('value/learnMore/<str:pk_test>/', views.valuePagelearnmore, name="user-learn-more"),
    path('account/', views.accountSettings, name="account"),
    path('profile/resultsdata/', views.resultsData, name="resultsdata"),  # add this for the graph
    path('compare/resultsdata_demographics/', views.resultsDataDemographics, name="resultsdata_demographics"),
    # add this for the graph demographics
    path('value/resultsdata_legislative/<str:pk_test>/', views.resultsDatalegislative, name="resultsdata_legislative"),
    # path('customer/', views.customer), # <----static path name
    path('customer/<str:pk_test>/', views.customer, name="customer"),  # dynamic display a paticualar customer

    # -----------------------------------entering deleting updating information from database----------------------

    # -------------------------------------password reset--------------------------------------------------------
    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
         name="reset_password"),  # Submit email form

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"),
         name="password_reset_done"),  # Email sent success message

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"),
         name="password_reset_confirm"),  # Link to password Rest form in email

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"),
         name="password_reset_complete"),  # Password successfully changed message

]
