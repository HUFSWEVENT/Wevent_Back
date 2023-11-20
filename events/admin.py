from django.contrib import admin
from .models import event, advertise

# Register your models here.

@admin.register(event)
class EventModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'host', 'host_email', 'date', 'deadline', 'event_image', 'user', 'created_at')

@admin.register(advertise)
class AdvertiseModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'host', 'host_email', 'content', 'ad_image', 'user')
