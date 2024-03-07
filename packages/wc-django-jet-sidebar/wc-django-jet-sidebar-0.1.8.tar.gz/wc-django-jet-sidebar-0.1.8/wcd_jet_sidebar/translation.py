from modeltranslation.translator import register, TranslationOptions

from .models import (
    SidebarItemConfig,
)

__all__ = (
    'SidebarItemConfigTranslationOptions',
)


@register(SidebarItemConfig)
class SidebarItemConfigTranslationOptions(TranslationOptions):
    fields = (
        'app_custom_name',
    )
