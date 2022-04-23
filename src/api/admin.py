import eatery.models as eatery_models
from django.contrib import admin

import api.models as models

# Register your models here.

admin.site.register(eatery_models.EateryStore)
admin.site.register(models.MenuStore)
admin.site.register(models.ItemStore)
admin.site.register(models.SubItemStore)
admin.site.register(models.AlertStore)
admin.site.register(models.CategoryStore)
admin.site.register(models.CategoryItemAssociation)
admin.site.register(models.RepeatingEventSchedule)
admin.site.register(models.ScheduleException)
admin.site.register(models.TransactionHistoryStore)
admin.site.register(models.ReportStore)
