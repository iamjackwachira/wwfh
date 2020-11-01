from collections import defaultdict

from django.db.models import Count
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.generic import DetailView, ListView, FormView


from .models import JobPost, Company
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
                    "title": job_post.title,
                    "company": job_post.company,
                    "get_job_type_display": job_post.get_job_type_display(),
                    "job_location": job_post.job_location,
                    "created_on": job_post.created_on,
                }
            )
        return dict(grouped_job_posts)


class JobCreateView(FormView):
    form_class = JobPostForm
    template_name = "jobs/job_create.html"

    def get_success_url(self):
        return reverse("jobs:jobs-home")

    def form_valid(self, form):
        company = Company()
        company.company_statement = form.cleaned_data.get("company_statement")
        company.description = form.cleaned_data.get("company_description")
        company.email = form.cleaned_data.get("company_email")
        company.logo = form.cleaned_data.get("company_logo")
        company.name = form.cleaned_data.get("company_name")
        company.url = form.cleaned_data.get("company_url")
        company.save()

        job_post = JobPost()
        job_post.company = company
        job_post.application_url = form.cleaned_data.get("job_application_url")
        job_post.description = form.cleaned_data.get("job_description")
        job_post.job_category = form.cleaned_data.get("job_category")
        job_post.job_location = form.cleaned_data.get("job_location")
        job_post.job_type = form.cleaned_data.get("job_type")
        job_post.regional_restrictions = form.cleaned_data.get(
            "job_regional_restrictions"
        )
        job_post.title = form.cleaned_data.get("job_title")
        job_post.save()
        return redirect(self.get_success_url())


class JobDetailView(DetailView):
    model = JobPost
    template_name = "jobs/job_detail.html"
    context_object_name = "job_post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_post = self.get_object()
        related_jobs = JobPost.objects.filter(
            job_category=job_post.job_category
        ).exclude(id=job_post.id)
        context["posts"] = related_jobs
        return context
