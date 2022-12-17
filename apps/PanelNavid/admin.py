from django.contrib import admin
from .models import SiteSettings,Message,InfoDeveloper

admin.site.register(InfoDeveloper)

admin.site.register(SiteSettings)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id','user')