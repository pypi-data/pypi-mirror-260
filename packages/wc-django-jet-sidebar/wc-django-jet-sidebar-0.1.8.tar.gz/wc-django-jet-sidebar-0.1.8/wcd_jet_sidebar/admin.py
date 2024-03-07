from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from modeltranslation.admin import TabbedDjangoJqueryTranslationAdmin

from .models import SidebarItemConfig


__all__ = ('SidebarItemConfigAdmin',)


@admin.register(SidebarItemConfig)
class SidebarItemConfigAdmin(SortableAdminMixin, TabbedDjangoJqueryTranslationAdmin, admin.ModelAdmin):
    list_display = ('sort_order', 'app', 'app_custom_name', 'position', 'view_type', 'is_global', )
    list_filter = ('app', 'position', 'view_type', 'user')
    search_fields = ('app', 'position', 'view_type')
    list_display_links = [
        'sort_order',
        'app',
    ]
    ordering = ('sort_order',)
    list_per_page = 20
    readonly_fields = ('user',)

    def save_model(self, request, obj, form, change):
        if not obj.user:
            obj.user = request.user.pk
        super().save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        temp_obj = SidebarItemConfig()
        temp_obj.add_registered_apps_to_choices()
        form = super().get_form(request, obj, **kwargs)
        return form

