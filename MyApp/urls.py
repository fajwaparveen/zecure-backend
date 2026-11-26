"""Intrusion_Detection URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from MyApp import views

urlpatterns = [
    path('login_get/', views.login_get),
    path('adm_login_post/', views.adm_login_post),
    path('adm_changepassword/', views.adm_changepassword),
    path('adm_changepassword_post/', views.adm_changepassword_post),
    path('adm_viewuser/', views.adm_viewuser),
    path('adm_addexpert/', views.adm_addexpert),
    path('adm_addexpert_post/', views.adm_addexpert_post),
    path('adm_appreview/', views.adm_appreview),
    path('adm_editexpert/<id>', views.adm_editexpert),
    path('adm_editexpert_post/', views.adm_editexpert_post),
    path('adm_sentreply/<id>', views.adm_sentreply),
    path('adm_sentreply_post/', views.adm_sentreply_post),
    path('adm_viewcomplaint/', views.adm_viewcomplaint),
    path('adm_viewexpert/', views.adm_viewexpert),
    path('adm_home/', views.adm_home),
    path('expert_addvideo/', views.expert_addvideo),
    path('expert_addvideo_post/', views.expert_addvideo_post),
    path('expert_editvideo/<id>', views.expert_editvideo),
    path('expert_editvideo_post/', views.expert_editvideo_post),
    path('expert_viewprofile/', views.expert_viewprofile),
    path('expert_viewvideo/', views.expert_viewvideo),
    path('expert_viewuser/', views.expert_viewuser),
    path('expert_home/', views.expert_home),
    path('log_out/', views.log_out),
    path('adm_deleteexpert/<id>',views.adm_deleteexpert),
    path('expert_deletevideo/<id>',views.expert_deletevideo),
    path('user_singup/',views.user_singup),
    path('user_login/',views.user_login),
    path('user_changepassword_post/',views.user_changepassword_post),
    path('user_view_profile/',views.user_view_profile),
    path('user_editprofile/',views.user_editprofile),
    path('user_sendcomplaint/',views.user_sendcomplaint),
    path('user_sendreview/',views.user_sendreview),
    path('user_viewexpert/',views.user_viewexpert),
    path('user_viewreply/',views.user_viewreply),
    path('user_viewvideo/',views.user_viewvideo),
    path('user_viewlogs/', views.user_viewlogs),
    path('send_request/',views.send_request),
    path('user_ViewRequestStatus/',views.user_ViewRequestStatus),
    path('expert_ViewRequest/',views.expert_ViewRequest),
    path('expert_ApproveRequest/<id>',views.expert_ApproveRequest),
    path('expert_RejectRequest/<id>', views.expert_RejectRequest),
    path('expert_ViewApprovedRequest/',views.expert_ViewApprovedRequest),
    path('expert_ViewRejectedRequest/',views.expert_ViewRejectedRequest),
    path('expert_changepassword/', views.expert_changepassword),
    path('web_forgetpassword/', views.web_forgetpassword),
    path('forgotpassword_post/', views.forgotpassword_post),
    path('android_forget_password_post/', views.android_forget_password_post),



]

