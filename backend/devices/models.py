from django.db import models

class Device(models.Model):
    """边缘设备/网关元数据"""
    name = models.CharField("设备名称", max_length=100)
    # device_uid 是硬件指纹，例如 MAC 地址或序列号
    device_uid = models.CharField("设备唯一码", max_length=64, unique=True)
    ip_address = models.GenericIPAddressField("IP地址", null=True, blank=True)
    is_active = models.BooleanField("是否启用", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.device_uid})"

class Telemetry(models.Model):
    """时序遥测数据 (温度、转速等)"""
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='telemetries')
    # 使用 JSONField 存储灵活的数据结构，例如 {"temp": 60, "rpm": 1500}
    data = models.JSONField("遥测数据") 
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f"{self.device.name} - {self.timestamp}"

class AlarmLog(models.Model):
    """AI 视觉报警记录"""
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    alarm_type = models.CharField("报警类型", max_length=50) # 例如 "fire" (火灾), "no_mask" (未戴帽)
    confidence = models.FloatField("AI置信度")
    # 报警时的现场抓拍图
    image = models.ImageField("现场截图", upload_to='alarms/%Y/%m/')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ALARM: {self.alarm_type} at {self.timestamp}"