import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from jobs.models import Company, JobPost
from jobs.choices import JOB_CATEGORY_CHOICES, JOB_TYPE_CHOICES, REGIONAL_RESTRICTIONS_CHOICES
from jobs.forms import JobPostForm


def create_job(title, category, company, **kwargs):
    return JobPost.objects.create(
        title=title,
        description=kwargs.get('description', 'A description'),
        job_type=kwargs.get('job_type', 'full_time'),
        job_location=kwargs.get('location', 'US'),
        job_category=category,
        regional_restrictions=kwargs.get('regional_restrictions', 'anywhere'),
        application_url=kwargs.get('', 'email@domain.com'),
        company=company
    )


class CompanyModelTests(TestCase):
    def test_num_jobs_posted(self):
        test_company = Company.objects.create(
            name="Company A",
            company_statement="Statement",
            headquarters="US",
            url="https://www.companya.com",
            email="email@domain.com",
            description="A description",
        )
        job_post_1 = create_job(title="Job A",
                                category=JOB_CATEGORY_CHOICES.design,
                                company=test_company)
        job_post_12 = create_job(title="Job B",
                                 category=JOB_CATEGORY_CHOICES.programming,
                                 company=test_company)
        self.assertIs(test_company.num_jobs_posted, 2)


class JobsViewTests(TestCase):
    def setUp(self):
        self.test_company = Company.objects.create(
            name="Company A",
            company_statement="Statement",
            headquarters="US",
            url="https://www.companya.com",
            email="email@domain.com",
            description="A description",
        )

    def test_no_jobs(self):
        response = self.client.get(reverse('jobs:jobs-home'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['job_posts'], {})

    def test_grouped_jobs_categories(self):
        """
        Job posts should be grouped by category
        """

        job_post_1 = create_job(title="Job A", category=JOB_CATEGORY_CHOICES.design,
                                company=self.test_company)
        job_post_2 = create_job(title="Job B", category=JOB_CATEGORY_CHOICES.programming,
                                company=self.test_company)
        job_post_3 = create_job(title="Job C", category=JOB_CATEGORY_CHOICES.design,
                                company=self.test_company)
        response = self.client.get(reverse('jobs:jobs-home'))
        self.assertEqual(len(response.context['job_posts']), 2)
        self.assertEqual(len(response.context['job_posts']['Programming']), 1)
        self.assertEqual(len(response.context['job_posts']['Design']), 2)

    def test_filter_jobs_by_category(self):
        """
        Job posts should be filtered correctly by category
        """
        job_post_1 = create_job(title="Job A", category=JOB_CATEGORY_CHOICES.design,
                                company=self.test_company)
        response = self.client.get(reverse('jobs:jobs-home'), {'job_category': JOB_CATEGORY_CHOICES.design})
        self.assertEqual(len(response.context['job_posts']), 1)
        response = self.client.get(reverse('jobs:jobs-home'), {'job_category': JOB_CATEGORY_CHOICES.programming})
        self.assertEqual(len(response.context['job_posts']), 0)

    def test_filter_jobs_by_job_type(self):
        """
        Job posts should be filtered correctly by job_type
        """
        job_post_1 = create_job(title="Job A", category=JOB_CATEGORY_CHOICES.design,
                                company=self.test_company, job_type=JOB_TYPE_CHOICES.full_time)
        response = self.client.get(reverse('jobs:jobs-home'), {'job_type': JOB_TYPE_CHOICES.full_time})
        self.assertEqual(len(response.context['job_posts']), 1)
        response = self.client.get(reverse('jobs:jobs-home'), {'job_type': JOB_TYPE_CHOICES.contract})
        self.assertEqual(len(response.context['job_posts']), 0)

    def test_filter_jobs_by_regional_restrictions(self):
        """
        Job posts should be filtered correctly by regional_restrictions
        """
        job_post_1 = create_job(title="Job A", category=JOB_CATEGORY_CHOICES.design,
                                company=self.test_company, regional_restrictions=REGIONAL_RESTRICTIONS_CHOICES.anywhere)
        response = self.client.get(reverse('jobs:jobs-home'),
                                   {'regional_restrictions': REGIONAL_RESTRICTIONS_CHOICES.anywhere})
        self.assertEqual(len(response.context['job_posts']), 1)
        response = self.client.get(reverse('jobs:jobs-home'),
                                   {'regional_restrictions': REGIONAL_RESTRICTIONS_CHOICES.usa_only})
        self.assertEqual(len(response.context['job_posts']), 0)

    def test_header_name_context(self):
        """
        The context "header_name" should be set correctly
        """
        response = self.client.get(reverse('jobs:jobs-home'),
                                   {'regional_restrictions': REGIONAL_RESTRICTIONS_CHOICES.anywhere})
        self.assertEqual(response.context['header_name'], "Anywhere (100% Remote Only)")
        response = self.client.get(reverse('jobs:jobs-home'),
                                   {'job_type': JOB_TYPE_CHOICES.full_time})
        self.assertEqual(response.context['header_name'], "Full Time")
        response = self.client.get(reverse('jobs:jobs-home'),
                                   {'job_category': JOB_CATEGORY_CHOICES.design})
        self.assertEqual(response.context['header_name'], "Design")

    def test_related_jobs(self):
        """
        When viewing one job, related jobs should be correct
        """
        job_post_1 = create_job(title="Job 1", category=JOB_CATEGORY_CHOICES.design,
                                company=self.test_company)
        job_post_2 = create_job(title="Job 2", category=JOB_CATEGORY_CHOICES.design,
                                company=self.test_company)
        response = self.client.get(reverse('jobs:job-detail', kwargs={'pk': job_post_1.id}))
        self.assertQuerysetEqual(response.context['posts'], ['<JobPost: Job 2>'])

    def test_company_jobs(self):
        """
        When viewing one job, related jobs should be correct
        """
        job_post_1 = create_job(title="Job 1", category=JOB_CATEGORY_CHOICES.design,
                                company=self.test_company)
        job_post_2 = create_job(title="Job 2", category=JOB_CATEGORY_CHOICES.design,
                                company=self.test_company)
        response = self.client.get(reverse('jobs:company-detail', kwargs={'pk': self.test_company.id}))
        self.assertQuerysetEqual(response.context['posts'], ['<JobPost: Job 2>', '<JobPost: Job 1>'])


class JobPostFormTests(TestCase):
    def setUp(self):
        self.valid_form_data = {
            "job_title": "Job A",
            "job_application_url": "https://www.wwfh.com/apply/",
            "job_description": "description",
            "job_type": JOB_TYPE_CHOICES.contract,
            "job_location": "location",
            "job_category": JOB_CATEGORY_CHOICES.programming,
            "job_regional_restrictions": REGIONAL_RESTRICTIONS_CHOICES.anywhere,
            "company_name": "Company A",
            "company_statement": "statement",
            "company_url": "https://www.wwfh.com",
            "company_email": "email@domain.com",
            "company_description": "description",
        }

    def test_title_required(self):
        self.valid_form_data.pop('job_title')
        form = JobPostForm(data=self.valid_form_data)
        self.assertEqual(
            form.errors["job_title"], ["This field is required."]
        )

    def test_company_email_format(self):
        self.valid_form_data["company_email"] = "invalid"
        form = JobPostForm(data=self.valid_form_data)
        self.assertEqual(
            form.errors["company_email"], ["Enter a valid email address."]
        )

    def test_company_url_format(self):
        self.valid_form_data["company_url"] = "invalidurl"
        form = JobPostForm(data=self.valid_form_data)
        self.assertEqual(
            form.errors["company_url"], ["Enter a valid URL."]
        )
