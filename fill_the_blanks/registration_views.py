'''
Views for logging in/out/signing up.
'''

from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordChangeDoneView, PasswordResetConfirmView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView, PasswordResetDoneView
from django.views import generic
from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy

from django.contrib.sites.shortcuts import get_current_site

from .forms import CustomUserCreationForm

class Login(LoginView):
    '''
    Log in view.
    '''
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.redirect_field_name: self.get_redirect_url(),
            'site': current_site,
            'site_name': current_site.name,
            **(self.extra_context or {})
        })
        context['next'] = '/'
        return context

class Logout(LogoutView):
    template_name = 'registration/log_out.html'

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class ResetPasswordView(PasswordResetView):
    template_name = 'registration/password_reset.html'

class ResetPasswordDoneView(PasswordResetDoneView):
    template_name = 'registration/reset_password_done.html'

class ConfirmPasswordResetView(PasswordResetConfirmView):
    template_name = 'registration/confirm_password_reset.html'

class CompletePasswordResetView(PasswordResetCompleteView):
    template_name = 'registration/reset_password_complete.html'

class ChangePasswordView(PasswordChangeView):
    template_name = 'registration/change_password_form.html'

class ChangePasswordDoneView(PasswordChangeDoneView):
    template_name = 'registration/change_password_done.html'