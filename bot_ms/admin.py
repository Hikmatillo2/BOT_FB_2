from django.contrib import admin
from .models import BotUser
from import_export.admin import ExportActionMixin


@admin.register(BotUser)
class BotUserAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['telegram_id',
                    'name',
                    ]
