from django.contrib import admin
from .models import ContentTask

@admin.register(ContentTask)
class ContentTaskAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "platform", "scheduled_date", "status", "title")
    list_filter = ("platform", "status", "scheduled_date")
    search_fields = ("title", "caption", "user__email")
    ordering = ("-scheduled_date",)
