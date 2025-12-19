from django.contrib import admin
from django.urls import path, include  # 1. 引入 include

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # 2. 挂载 devices 的 API，前缀设为 api/v1/
    path('api/v1/', include('devices.urls')),
]