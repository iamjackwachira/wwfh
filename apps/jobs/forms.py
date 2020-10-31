from django import forms

from tinymce.widgets import TinyMCE

import jobs.choices as choices
from .models import Company, JobPost


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class JobPostForm(forms.Form):
    job_title = forms.CharField()
    job_application_url = forms.CharField()
    job_description = forms.CharField(widget=TinyMCEWidget())
    job_type = forms.ChoiceField(
        choices=choices.JOB_TYPE_CHOICES, widget=forms.RadioSelect
    )
    job_location = forms.CharField()
    job_category = forms.ChoiceField(choices=choices.JOB_CATEGORY_CHOICES)
    job_regional_restrictions = forms.ChoiceField(
        choices=choices.REGIONAL_RESTRICTIONS_CHOICES
    )
    company_name = forms.CharField()
    company_statement = forms.CharField()
    company_logo = forms.ImageField()
    company_url = forms.CharField()
    company_email = forms.EmailField()
    company_description = forms.CharField(widget=TinyMCE())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial["job_category"] = "programming"
        self.initial["job_type"] = "full_time"
        self.initial["job_regional_restrictions"] = "anywhere"
