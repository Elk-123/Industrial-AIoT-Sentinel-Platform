from django.contrib import admin
from .models import Device, Telemetry, AlarmLog

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'device_uid', 'ip_address', 'is_active', 'created_at')
    search_fields = ('name', 'device_uid')

@admin.register(Telemetry)
class TelemetryAdmin(admin.ModelAdmin):
    list_display = ('device', 'data', 'timestamp')
    list_filter = ('device', 'timestamp')

@admin.register(AlarmLog)
class AlarmLogAdmin(admin.ModelAdmin):
    list_display = ('device', 'alarm_type', 'confidence', 'timestamp')
    list_filter = ('alarm_type',)