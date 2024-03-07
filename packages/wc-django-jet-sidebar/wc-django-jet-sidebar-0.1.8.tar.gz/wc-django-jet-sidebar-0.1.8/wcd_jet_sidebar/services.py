from django.apps import apps
from django.utils.text import capfirst
from django.urls import reverse, resolve, NoReverseMatch
from django.utils.translation import ugettext_lazy as _

from collections import OrderedDict

from jet.models import PinnedApplication

from .models import SidebarItemConfig
from .utils import get_admin_site


__all__ = ('get_additional_menu_items', )


def user_is_authenticated(user):
    if not hasattr(user.is_authenticated, '__call__'):
        return user.is_authenticated
    else:
        return user.is_authenticated()


def get_app_models(name):
    all_models = apps.get_models()
    models_in_app = [model for model in all_models if model._meta.app_label == name]
    return models_in_app

def get_changed_list():
    top = SidebarItemConfig.objects.top()
    bottom = SidebarItemConfig.objects.bottom()
    
    top_apps = []
    top_apps.extend(get_app_models(item.app) for item in top)
    top_apps = [model for sublist in top_apps for model in sublist]

    bottom_apps = []
    bottom_apps.extend(get_app_models(item.app) for item in bottom)
    bottom_apps = [model for sublist in bottom_apps for model in sublist]

    return top_apps, bottom_apps


def get_app_list(context, order=True):
    admin_site = get_admin_site()
    request = context['request']

    app_dict = {}
    for model, model_admin in admin_site._registry.items():
        app_label = model._meta.app_label
        try:
            has_module_perms = model_admin.has_module_permission(request)
        except AttributeError:
            has_module_perms = request.user.has_module_perms(app_label) # Fix Django < 1.8 issue

        if has_module_perms:
            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True in perms.values():
                info = (app_label, model._meta.model_name)
                
                sidebar_app_config = SidebarItemConfig.objects.filter(app=app_label)

                sidebar_config_global = sidebar_app_config.filter(is_global=True).first()
                sidebar_config_for_user = sidebar_app_config.filter(user=request.user.pk, is_global=False).first()

                sidebar_config = sidebar_config_for_user if sidebar_config_for_user else sidebar_config_global

                model_dict = {
                    'name': capfirst(model._meta.verbose_name_plural),
                    'object_name': model._meta.object_name,
                    'perms': perms,
                    'model_name': model._meta.model_name,
                    
                }
                if perms.get('change', False) or perms.get('view', False):
                    try:
                        model_dict['admin_url'] = reverse('admin:%s_%s_changelist' % info, current_app=admin_site.name)
                    except NoReverseMatch:
                        pass
                if perms.get('add', False):
                    try:
                        model_dict['add_url'] = reverse('admin:%s_%s_add' % info, current_app=admin_site.name)
                    except NoReverseMatch:
                        pass
                if app_label in app_dict:
                    app_dict[app_label]['models'].append(model_dict)
                else:
                    try:
                        name = apps.get_app_config(app_label).verbose_name
                    except NameError:
                        name = app_label.title()
                    app_dict[app_label] = {
                        'name': name,
                        'app_label': app_label,
                        'app_url': reverse(
                            'admin:app_list',
                            kwargs={'app_label': app_label},
                            current_app=admin_site.name,
                        ),
                        'has_module_perms': has_module_perms,
                        'models': [model_dict],
                        'position': sidebar_config.position if sidebar_config else None,
                        'view_type': sidebar_config.view_type if sidebar_config else None,
                        'sort_order': sidebar_config.sort_order if sidebar_config else 0,
                        'custom_name': sidebar_config.app_custom_name if sidebar_config else '',
                    }
    app_list = list(app_dict.values())
    app_list.sort(key=lambda x: x['name'].lower())
    app_list.sort(key=lambda x: x['sort_order'])
    # Sort the models alphabetically within each app.
    for app in app_list:
        app['models'].sort(key=lambda x: x['name'])
    return app_list 

def transform_to_dict(app_list, pinned_apps):
    return map(lambda app: {
        'app_label': app['app_label'],
        'url': app['app_url'],
        'url_blank': False,
        'label': app.get('name', capfirst(_(app['app_label']))),
        'has_perms': app.get('has_module_perms', False),
        'models': list(map(lambda model: {
            'url': model.get('admin_url'),
            'url_blank': False,
            'name': model['model_name'],
            'object_name': model['object_name'],
            'label': model.get('name', model['object_name']),
            'has_perms': any(model.get('perms', {}).values()),
            'pinned': f'{app["app_label"]}_{model["model_name"]}' in pinned_apps,
        }, app['models'])),
        'pinned': f'{app["app_label"]}_parent' in pinned_apps,
        'pinned_parent': any(f'{app["app_label"]}_{model["model_name"]}' in pinned_apps for model in app['models']),
        'custom': False,
        'position': app['position'],
        'view_type': app['view_type'],
        'sort_order': app['sort_order'],
        'custom_name': app['custom_name'],
    }, app_list)


def get_original_menu_items(context):
    if context.get('user') and user_is_authenticated(context['user']):
        pinned_apps = PinnedApplication.objects.filter(user=context['user'].pk).values_list('app_label', flat=True)
    else:
        pinned_apps = []

    apps = get_app_list(context)
    apps = transform_to_dict(apps, pinned_apps)
    return apps



def get_additional_menu_items(context):
    pinned_apps = PinnedApplication.objects.filter(user=context['user'].pk).values_list('app_label', flat=True)
    original_app_list = OrderedDict(map(lambda app: (app['app_label'], app), get_original_menu_items(context)))

    def map_item(item):
        item['items'] = item['models']
        return item
    app_list = list(map(map_item, original_app_list.values()))

    current_found = False

    for app in app_list:
        if not current_found:
            for model in app['items']:
                if not current_found and model.get('url') and context['request'].path.startswith(model['url']):
                    model['current'] = True
                    current_found = True
                else:
                    model['current'] = False

            if not current_found and app.get('url') and context['request'].path.startswith(app['url']):
                app['current'] = True
                current_found = True
            else:
                app['current'] = False

    return app_list