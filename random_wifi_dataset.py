import json
import random
import time

import pywifi

# 配置随机指纹数据库的参数
NUM_REFERENCE_POINTS = 20  # 参考点的数量
NUM_WIFI_AP = 5            # WiFi AP的数量
AREA_SIZE = 10             # 室内区域大小


# 扫描WiFi
def scan_wifi_and_get_ssid_list():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(2)
    results = iface.scan_results()

    wifi_ap_ssid_rssi_list = {ap.ssid: ap.signal for ap in results if ap.ssid and ap.signal > -100}
    return wifi_ap_ssid_rssi_list


# 随机生成指纹数据库
def generate_random_fingerprint_db(wifi_ap_ssid_list):
    fingerprint_db = []

    for i in range(NUM_REFERENCE_POINTS):
        x = round(random.uniform(0, AREA_SIZE), 2)
        y = round(random.uniform(0, AREA_SIZE), 2)

        if i == 0:
            rssi_values = {ssid: wifi_ap_ssid_list[ssid] for ssid in wifi_ap_ssid_list}
        else:
            rssi_values = {ssid: random.randint(-90, -30) for ssid in wifi_ap_ssid_list}

        fingerprint_record = {
            "location": [x, y],
            "rssis": rssi_values,
            "ssids": {f"AP_{i+1}": ssid for i, ssid in enumerate(wifi_ap_ssid_list)}
        }

        fingerprint_db.append(fingerprint_record)

    return fingerprint_db


def save_fingerprint_db(fingerprint_db, filename="fingerprint_db.json"):
    with open(filename, 'w') as f:
        json.dump(fingerprint_db, f, indent=4)
    print(f"随机生成的指纹数据库已保存到文件：{filename}")


# 主函数
if __name__ == "__main__":
    # 扫描WiF并获取SSID列表
    wifi_ap_ssid_list = scan_wifi_and_get_ssid_list()
    print(f"扫描到的WiFi SSID列表：{wifi_ap_ssid_list}")

    if wifi_ap_ssid_list:
        fingerprint_db = generate_random_fingerprint_db(wifi_ap_ssid_list)

        # 打印部分生成的指纹数据
        # print("\n生成的部分随机指纹数据：")
        # for i in range(min(5, len(fingerprint_db))):  # 限制打印的数量
        #     print(fingerprint_db[i])

        # 保存到文件
        save_fingerprint_db(fingerprint_db)
    else:
        print("没有扫描到任何WiFi SSID，请确保WiFi处于开启状态并且周围有WiFi网络")
