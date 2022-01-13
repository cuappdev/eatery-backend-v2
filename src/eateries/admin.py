from django.contrib import admin

import eateries.models as models
# Register your models here.

admin.site.register(models.EateryStore)
admin.site.register(models.MenuStore)
admin.site.register(models.ItemStore)
admin.site.register(models.SubItemStore)
admin.site.register(models.AlertStore)
admin.site.register(models.CategoryStore)
admin.site.register(models.CategoryItemAssociation)
admin.site.register(models.DayOfWeekEventSchedule)
admin.site.register(models.DateEventSchedule)
admin.site.register(models.ClosedEventSchedule)
admin.site.register(models.TransactionHistoryStore)
admin.site.register(models.ReportStore)