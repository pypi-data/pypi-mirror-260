from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SidebarConfig(AppConfig):
    name = 'wcd_jet_sidebar'
    verbose_name = _('Admin Sidebar Config')

