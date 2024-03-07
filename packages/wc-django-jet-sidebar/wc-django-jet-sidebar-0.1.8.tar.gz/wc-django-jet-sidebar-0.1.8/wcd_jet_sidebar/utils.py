from django.contrib import admin
from django.urls import reverse, resolve

__all__ = ('get_registered_apps', )


def get_admin_site():
    site = admin.site
    index_resolver = resolve(reverse('admin:index'))
    if hasattr(index_resolver.func, 'admin_site'):
        site = index_resolver.func.admin_site
    return site

def get_registered_apps():
    site = get_admin_site()
    registered_models = site._registry.items()
    choices = list(set([(model._meta.app_config.label, model._meta.app_config.verbose_name) for model, _ in registered_models]))
    sorted_choices = sorted(choices, key=lambda x: x[1])
    return sorted_choices
