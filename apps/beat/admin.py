from django.contrib import admin
from .models import *
from .models import BeatHits
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(Beat)
class BeatAdmin(admin.ModelAdmin):
    exclude = ('code','time_audio')