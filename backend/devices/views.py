from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import Device, Telemetry
from django.shortcuts import render

class DeviceHeartbeatView(APIView):
    """
    接收边缘端数据上报
    Endpoint: POST /api/v1/telemetry/
    数据格式: {"uid": "SIM001", "data": {"temp": 60, "rpm": 1200}}
    """
    def post(self, request):
        # 1. 获取请求参数
        uid = request.data.get('uid')
        payload = request.data.get('data')

        if not uid or not payload:
            return Response({"error": "缺少 uid 或 data 字段"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. 【缓存策略】检查设备是否存在
        # 为了不每次都查数据库，我们将 device_id 存入 Redis
        cache_key = f"device_id_{uid}"
        device_id = cache.get(cache_key)

        if not device_id:
            try:
                # 缓存没命中，去数据库查
                device = Device.objects.get(device_uid=uid)
                device_id = device.id
                # 查到后写入缓存，有效期 1 小时
                cache.set(cache_key, device.id, 3600)
            except Device.DoesNotExist:
                return Response({"error": f"设备 {uid} 未注册"}, status=status.HTTP_404_NOT_FOUND)

        # 3. 【心跳机制】更新在线状态
        # 只要有数据发过来，就标记为 online，有效期 60秒
        # 如果60秒没数据，Redis Key 自动消失，前端就知道设备离线了
        cache.set(f"device_online_{uid}", "online", 60)

        # 4. 数据入库 (PostgreSQL)
        Telemetry.objects.create(device_id=device_id, data=payload)

        return Response({"status": "received", "device": uid}, status=status.HTTP_200_OK)


class DashboardDataView(APIView):
    """
    提供给前端图表的 API
    返回指定设备的最后 20 条数据
    """
    def get(self, request):
        uid = request.query_params.get('uid', 'SIM001')
        
        # 查询最近的 20 条记录 (按时间倒序)
        logs = Telemetry.objects.filter(
            device__device_uid=uid
        ).order_by('-timestamp')[:20]
        
        # 整理成前端 ECharts 需要的列表格式 (时间正序)
        times = [log.timestamp.strftime("%H:%M:%S") for log in reversed(logs)]
        temps = [log.data.get('temp', 0) for log in reversed(logs)]
        
        return Response({
            "times": times,
            "temps": temps
        })

def dashboard_view(request):
    """
    渲染 HTML 页面
    """
    return render(request, 'devices/dashboard.html')