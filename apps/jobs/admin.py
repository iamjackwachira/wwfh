from django.contrib import admin

from .models import JobPost, Company


class JobPostAdmin(admin.ModelAdmin):
    list_display = ("title", "job_type", "job_category", "company")
    display = "Job Post"


class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "url", "email")
    display = "Company"


admin.site.register(JobPost, JobPostAdmin)
admin.site.register(Company, CompanyAdmin)
