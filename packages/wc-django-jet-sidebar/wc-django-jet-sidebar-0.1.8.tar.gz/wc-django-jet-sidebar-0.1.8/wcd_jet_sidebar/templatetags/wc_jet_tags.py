from django import template
from ..services import get_additional_menu_items

__all__ = ('jet_additional_menu_items', ) 

register = template.Library()
assignment_tag = register.assignment_tag if hasattr(register, 'assignment_tag') else register.simple_tag

@assignment_tag(takes_context=True)
def jet_additional_menu_items(context):
    return get_additional_menu_items(context)