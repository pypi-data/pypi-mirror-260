from django.utils.translation import pgettext_lazy

from model_utils import Choices

__all__ = (
  'SIDEBAR_POSITION_CHOICES',
  'SIDEBAR_VIEW_CHOICES',
)


SIDEBAR_POSITION_CHOICES = Choices(
    ('top', 'Top'),
    ('bottom', 'Bottom'),
) 

SIDEBAR_VIEW_CHOICES = Choices(
    ('expanded', 'Expanded'),
    ('collapse', 'Collapse'),
) 