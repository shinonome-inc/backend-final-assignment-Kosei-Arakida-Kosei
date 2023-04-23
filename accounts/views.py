from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from .forms import SignupForm

User = get_user_model()


class SignupView(CreateView):
    form_class = SignupForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy(settings.LOGIN_REDIRECT_URL)

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=username, email=email, password=password)
        if user is not None:
            login(self.request, user)
        return response


class LoginView(auth_views.LoginView):
    template_name = "accounts/login.html"


class LogoutView(LoginRequiredMixin, auth_views.LogoutView):
    pass


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/user_profile.html"
