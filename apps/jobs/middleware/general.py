from collections import namedtuple
from django.conf import settings

from jobs.choices import JOB_CATEGORY_CHOICES, JOB_TYPE_CHOICES


class SharedContextMiddleware:
    """
    Middleware class that injects common data that's needed
    when rendering most of view responses into the context
    of the template_response objects returned by the views.
    The injected data includes:
    categories: includes a listing of all job categories
    including job types
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_template_response(self, request, response):
        """
        Middleware hook method called immediately after the
        view function returns a response.
        """
        categories = []
        Category = namedtuple("Category", ["slug", "name"])
        for item in JOB_CATEGORY_CHOICES:
            categories.append(Category(item[0], name=item[1]))

        for item in JOB_TYPE_CHOICES:
            categories.append(Category(item[0], name=item[1]))

        response.context_data.update({"categories": categories})
        return response