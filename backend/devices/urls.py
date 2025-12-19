from django.urls import path
from .views import DeviceHeartbeatView, DashboardDataView, dashboard_view

urlpatterns = [
    # 数据上报接口
    path('telemetry/', DeviceHeartbeatView.as_view()),
    
    # 前端获取图表数据的接口
    path('dashboard/data/', DashboardDataView.as_view()),
    
    # 浏览器直接访问的页面
    path('dashboard/', dashboard_view),
]