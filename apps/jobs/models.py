from django.db import models

from core.models import BaseModel
from tinymce.models import HTMLField
import jobs.choices as choices


class JobPost(BaseModel):
    """ Job Post """

    title = models.CharField(max_length=200)
    description = HTMLField()
    job_type = models.CharField(choices=choices.JOB_TYPE_CHOICES, max_length=100)
    job_location = models.CharField(max_length=200)
    job_category = models.CharField(
        choices=choices.JOB_CATEGORY_CHOICES, max_length=100
    )
    regional_restrictions = models.CharField(
        choices=choices.REGIONAL_RESTRICTIONS_CHOICES, max_length=100
    )
    application_url = models.CharField(max_length=200)
    company = models.ForeignKey(
        "Company", on_delete=models.CASCADE, related_name="job_posts"
    )

    class Meta:
        ordering = ["-created_on"]
        verbose_name = "Job Post"
        verbose_name_plural = "Job Posts"

    def __str__(self):
        return self.title


class Company(BaseModel):
    """ Company posting the job """

    name = models.CharField(max_length=200)
    company_statement = models.CharField(max_length=500)
    headquarters = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="company_uploads/", blank=True, null=True)
    url = models.CharField(max_length=200)
    email = models.CharField(max_length=200, blank=True, null=True)
    description = HTMLField()

    class Meta:
        ordering = ["-created_on"]
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name
