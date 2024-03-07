from django.db import models

from .consts import SIDEBAR_POSITION_CHOICES, SIDEBAR_VIEW_CHOICES


__all__ = ('SidebarItemQuerySet', ) 

class SidebarItemQuerySet(models.QuerySet):
    def top(self):
        return self.filter(position=SIDEBAR_POSITION_CHOICES.top)
    
    def bottom(self):
        return self.filter(position=SIDEBAR_POSITION_CHOICES.bottom)
    
    def expanded(self):
        return self.filter(position=SIDEBAR_VIEW_CHOICES.expanded)
    
    def collapse(self):
        return self.filter(position=SIDEBAR_VIEW_CHOICES.collapse)