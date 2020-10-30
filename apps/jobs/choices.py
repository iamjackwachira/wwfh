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

REGIONAL_RESTRICTIONS_CHOICES = Choices(
    ("anywhere", _("Anywhere (100% Remote Only)")),
    ("usa_only", _("USA Only")),
    ("north_america_only", _("North America Only")),
    ("europe_only", _("Europe Only")),
    ("americas_only", _("Americas Only")),
    ("canada_only", _("Canada Only")),
    ("emea_only", _("EMEA Only")),
    ("asia_only", _("Asia Only")),
    ("africa_only", _("Africa Only")),
    ("other", _("Other")),
)
