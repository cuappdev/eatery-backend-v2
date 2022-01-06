from django.contrib import admin

from eateries.models import EateryStore, MenuItemStore, MenuSubItemStore, MenuStore, ExceptionStore, ForSale, RepeatingEventSchedule, EventChangeLog
# Register your models here.

admin.site.register(EateryStore)
admin.site.register(MenuStore)
admin.site.register(MenuItemStore)
admin.site.register(MenuSubItemStore)
admin.site.register(ExceptionStore)
admin.site.register(ForSale)
admin.site.register(RepeatingEventSchedule)
admin.site.register(EventChangeLog)