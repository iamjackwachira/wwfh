from collections import defaultdict

from django.db.models import Count
from django.shortcuts import render
from django.views.generic import ListView, FormView

from .models import JobPost
from .forms import JobPostForm


class JobListView(ListView):
    model = JobPost
    template_name = "jobs/job_list.html"
    context_object_name = "job_posts"

    def get_queryset(self):
        queryset = super().get_queryset()
        grouped_job_posts = defaultdict(list)
        for job_post in queryset.iterator():
            grouped_job_posts[job_post.job_category].append(
                {
                    "job_title": job_post.title,
                    "company_name": job_post.company.name,
                    "company_logo": job_post.company.logo.url,
                    "job_type": job_post.get_job_type_display(),
                    "job_location": job_post.job_location,
                    "date_posted": job_post.created_on,
                }
            )
        return dict(grouped_job_posts)


class JobCreateView(FormView):
    form_class = JobPostForm
    template_name = "jobs/job_create.html"

    def get_success_url(self):
        return reverse("jobs:job_list")

    def form_valid(self, form):
        form.save()
        return redirect(self.get_success_url())
