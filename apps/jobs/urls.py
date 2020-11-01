from django.urls import path

from . import views

app_name = "jobs"

urlpatterns = [
    path("", views.JobListView.as_view(), name="jobs-home"),
    path("jobs/new/", views.JobCreateView.as_view(), name="job-create"),
    path("jobs/<int:pk>/", views.JobDetailView.as_view(), name="job-detail"),
    path(
        "companies/<int:pk>/", views.CompanyDetailView.as_view(), name="company-detail"
    ),
]
