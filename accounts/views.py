from django.conf import settings
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from tweets.models import Tweet

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


class UserProfileView(LoginRequiredMixin, ListView):
    template_name = "accounts/user_profile.html"
    model = Tweet
    slug_field = "username"
    slug_url_kwargs = "username"
    context_object_name = "tweets"

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs["username"])
        return Tweet.objects.select_related("user").filter(user=user)
