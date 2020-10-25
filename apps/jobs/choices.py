from model_utils import Choices
from django.utils.translation import ugettext_lazy as _


JOB_TYPE_CHOICES = Choices(
    ("full_time", _("Full Time")),
    ("contract", _("Contract")),
)

JOB_CATEGORY_CHOICES = Choices(
    ("design", _("Design")),
    ("programming", _("Programming")),
    ("customer_support", _("Customer Support")),
    ("copy_writing", _("Copy Writing")),
    ("devops_sys_admin", _("DevOps and Sysadmin")),
    ("sales_marketing", _("Sales and Marketing")),
    ("business_mgmt_finance", _("Business Management and Finance")),
    ("product", _("Product")),
    ("other", _("All Other Remote")),
)