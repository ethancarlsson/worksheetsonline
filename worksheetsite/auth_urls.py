'''
All the auth related views.
'''

from django.contrib.auth import views
from django.urls import path
from fill_the_blanks import registration_views

urlpatterns = [
    path('login/', registration_views.Login.as_view(), name='login'),
    path('logout/', registration_views.Logout.as_view(), name='logout'),
    path('signup/', registration_views.SignUpView.as_view(), name='signup'),


    path('password_change/', registration_views.ChangePasswordView.as_view(), name='password_change'),
    path('password_change/done/',
        registration_views.ChangePasswordDoneView.as_view(), name='password_change_done'),

    path('password_reset/', registration_views.ResetPasswordView.as_view(), name='password_reset'),
    path('password_reset/done/', registration_views.ResetPasswordDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        registration_views.ConfirmPasswordResetView.as_view(), name='password_reset_confirm'),
    path('reset/done/', registration_views.CompletePasswordResetView.as_view(), name='password_reset_complete'),
]
