from django.shortcuts import render
from django.views.generic import ListView

from .models import JobPost


class HomePageView(ListView):
    model = JobPost
    template_name = "base.html"
    context_object_name = "job_posts"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
