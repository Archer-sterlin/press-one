from django.contrib import admin

# Register your models here.
from .models import Item


class ItemAdmin(admin.ModelAdmin):
    search_fields = ["id", "name", "description", "price"]
    list_display = ("id", "name", "description", "price")
    list_per_page = 100


admin.site.register(Item, ItemAdmin)
