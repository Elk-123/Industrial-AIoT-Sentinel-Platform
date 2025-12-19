import time
import requests
import random
import json
import sys

# --- 配置区 ---
# 后端接口地址 (确保 Django 正在运行)
SERVER_URL = "http://127.0.0.1:8000/api/v1/telemetry/"
# 设备唯一码 (必须与你刚才在 Django 后台创建的一致)
DEVICE_UID = "SIM001" 

def simulate_plc_read():
    """
    模拟从 PLC (可编程逻辑控制器) 读取传感器数据
    """
    # 模拟设备温度：在 60℃ 左右波动
    temp = 60 + random.uniform(-5, 5)
    # 模拟电机转速：在 1000-3000 转之间变化
    rpm = random.randint(1000, 3000)
    # 模拟电压
    voltage = 220 + random.uniform(-2, 2)
    
    return {
        "temp": round(temp, 2),
        "rpm": rpm,
        "voltage": round(voltage, 1)
    }

def simulate_ai_inference():
    """
    模拟 YOLOv8 视觉算法的检测结果
    返回: True (有火灾) / False (安全)
    """
    # 假设有 5% 的概率检测到火灾异常
    if random.random() < 0.05:
        return True
    return False

def main():
    print(f"🚀 [启动] 边缘智能网关模拟器 | 设备ID: {DEVICE_UID}")
    print(f"📡 [目标] {SERVER_URL}")
    print("-" * 40)

    try:
        while True:
            # 1. 采集数据 (Modbus)
            sensor_data = simulate_plc_read()
            
            # 2. AI 视觉检测
            has_fire = simulate_ai_inference()
            
            # 如果检测到火灾，添加报警标记 (这里简化处理，实际会上传图片)
            if has_fire:
                print("🔥 [警告] AI 视觉检测到火灾隐患！")
                sensor_data['alarm'] = 'fire_detected'
            
            # 3. 组装数据包
            payload = {
                "uid": DEVICE_UID,
                "data": sensor_data
            }
            
            # 4. 发送 HTTP 请求
            start_time = time.time()
            try:
                response = requests.post(SERVER_URL, json=payload, timeout=2)
                latency = (time.time() - start_time) * 1000
                
                if response.status_code == 200:
                    print(f"✅ [上传成功] {latency:.0f}ms | 数据: {sensor_data}")
                else:
                    print(f"❌ [服务器拒绝] {response.status_code} | {response.text}")
                    
            except requests.exceptions.ConnectionError:
                print("⚠️ [连接失败] 无法连接到服务器，请检查 Django 是否运行！")

            # 5. 模拟采样频率 (每 2 秒一次)
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n🛑 [停止] 模拟器已关闭")
        sys.exit(0)

if __name__ == "__main__":
    main()