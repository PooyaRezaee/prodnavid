from django.contrib import admin
from .models import IpLog,BlockListIp

@admin.register(IpLog)
class ViewAdmin(admin.ModelAdmin):
    list_display = ('ip_addr','route','created')
    list_filter = ('ip_addr','created')
    search_fields = ('ip_addr','route','created')

@admin.register(BlockListIp)
class ViewAdmin(admin.ModelAdmin):
    pass