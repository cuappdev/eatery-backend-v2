from django.contrib import admin

from api.models import MenuModel as models

admin.site.register(models.MenuStore)
admin.site.register(models.ItemStore)
admin.site.register(models.SubItemStore)
admin.site.register(models.CategoryStore)
admin.site.register(models.CategoryItemAssociation)
#admin.site.register(models.RepeatingEventSchedule)
#admin.site.register(models.ScheduleException)
#admin.site.register(models.TransactionHistoryStore)
