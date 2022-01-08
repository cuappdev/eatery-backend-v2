from django.contrib import admin

from eateries.models import EateryStore, ItemStore, SubItemStore, CategoryStore, MenuStore, ExceptionStore, CategoryItemAssociation, EventSchedule, DayOfWeekEventSchedule, DateEventSchedule, ClosedEventSchedule
# Register your models here.

admin.site.register(EateryStore)
admin.site.register(MenuStore)
admin.site.register(ItemStore)
admin.site.register(SubItemStore)
admin.site.register(ExceptionStore)
admin.site.register(CategoryStore)
admin.site.register(CategoryItemAssociation)
admin.site.register(EventSchedule)
admin.site.register(DayOfWeekEventSchedule)
admin.site.register(DateEventSchedule)
admin.site.register(ClosedEventSchedule)