from django.db import models
from django.utils.translation import pgettext_lazy

from ..consts import SIDEBAR_POSITION_CHOICES, SIDEBAR_VIEW_CHOICES
from ..utils import get_registered_apps
from ..querysets import SidebarItemQuerySet

__all__ = ('SidebarItemConfig', )


class SidebarItemConfig(models.Model):
    sort_order = models.PositiveIntegerField(
        verbose_name=pgettext_lazy('wcd_jet_sidebar', 'Sort order'),
        editable=True, db_index=True, null=True, default=1,
    )
    app = models.CharField(
        verbose_name=pgettext_lazy('wcd_jet_sidebar', 'Apps'),
        max_length=255,
        choices=[],
        blank=False,
        null=True,
        help_text=pgettext_lazy('wcd_jet_sidebar', 'Select app for which the sidebar will be displayed')
    )
    app_custom_name = models.CharField(
        verbose_name=pgettext_lazy('wcd_jet_sidebar', 'App custom name'),
        max_length=255,
        blank=True,
        null=True,
        help_text=pgettext_lazy('wcd_jet_sidebar', 'Custom name for the app. If not provided, the app name will be used.')
    )
    position = models.CharField(
        pgettext_lazy('wcd_jet_sidebar', 'Position'),
        max_length=255,
        choices=SIDEBAR_POSITION_CHOICES,
        blank=True,
        null=True,
        help_text=pgettext_lazy('wcd_jet_sidebar',
                                'Position of the this item in sidebar. '),
    )
    view_type = models.CharField(
        pgettext_lazy('wcd_jet_sidebar', 'View type'),
        choices=SIDEBAR_VIEW_CHOICES,
        max_length=255,
        blank=True,
        null=True,
        help_text=pgettext_lazy('wcd_jet_sidebar',
                                'View type of the this item in sidebar.'),
    )
    user = models.PositiveIntegerField(verbose_name=pgettext_lazy('wcd_jet_sidebar', 'User'),)
    is_global = models.BooleanField(
        pgettext_lazy('wcd_jet_sidebar', 'Is global'),
        help_text=pgettext_lazy('wcd_jet_sidebar', 'Global sidebar item for all users. If checked, the user field will be ignored.'),
        default=False
    )

    objects = SidebarItemQuerySet.as_manager()

    def add_registered_apps_to_choices(self):
        app_choices = get_registered_apps()
        self._meta.get_field('app').choices = app_choices

    class Meta:
        verbose_name = pgettext_lazy('wcd_jet_sidebar', 'Sidebar item config')
        verbose_name_plural = pgettext_lazy('wcd_jet_sidebar', 'Sidebar item configs')
        ordering = ['sort_order']

    def __str__(self):
        return f'{self.app} - {self.position} - {self.view_type}'
    