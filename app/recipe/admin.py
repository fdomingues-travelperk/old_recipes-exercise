from django.contrib import admin

from recipe import models

admin.site.register(models.Recipe)
admin.site.register(models.Ingredient)
