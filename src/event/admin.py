from django.contrib import admin
from event.models import CategoryItemAssociation, Menu, Item, SubItem, Category

admin.site.register(Menu)
admin.site.register(Item)
admin.site.register(SubItem)
admin.site.register(Category)
admin.site.register(CategoryItemAssociation)

#admin.site.register(models.RepeatingEventSchedule)
#admin.site.register(models.ScheduleException)
#admin.site.register(models.TransactionHistoryStore)
