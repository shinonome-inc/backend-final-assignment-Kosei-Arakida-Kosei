from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin

from .models import Tweet


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "tweets/home.html"
    model = Tweet

    def get_queryset(self):
        return Tweet.objects.exclude(user=self.request.user)


class TweetCreateView(LoginRequiredMixin, CreateView):
    template_name = "tweets/create.html"
    fields = ["title", "content"]
    model = Tweet
    success_url = reverse_lazy("tweets/home.html")

    def homevalid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TweetDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Tweet
    template_name = "tweets/detail.html"


class TweetDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "tweets/delete.html"

    def test_func(self, **kwargs):
        pk = self.kwargs["pk"]
        post = Tweet.objects.get(pk=pk)
        return post.user == self.request.user
