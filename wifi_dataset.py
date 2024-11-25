import pywifi
import time
import json


# WiFi扫描函数
def scan_wifi():
    wifi = pywifi.PyWiFi()
    iface = wifi.interfaces()[0]
    iface.scan()
    time.sleep(2)
    results = iface.scan_results()

    ap_list = {}
    for ap in results:
        ssid = ap.ssid
        rssi = ap.signal
        if ssid:
            ap_list[ssid] = rssi
    return ap_list


# 指纹数据采集函数
def collect_fingerprint_data():
    fingerprint_db = []
    while True:
        try:
            x = float(input("请输入当前位置的 X 坐标："))
            y = float(input("请输入当前位置的 Y 坐标："))
            print("正在扫描 WiFi，请稍候...")
            rssi_data = scan_wifi()
            print(f"当前位置 ({x}, {y}) 的 WiFi RSSI 数据：{rssi_data}")

            # 保存当前位置和 RSSI 数据
            fingerprint_record = {
                "location": [x, y],
                "rssis": rssi_data,
                "ssids": {f"AP_{i + 1}": ssid for i, ssid in enumerate(rssi_data.keys())}
            }
            fingerprint_db.append(fingerprint_record)

            # 是否继续采集
            cont = input("是否继续采集下一个位置的数据？(y/n): ")
            if cont.lower() != 'y':
                break
        except Exception as e:
            print(f"采集数据时出错：{e}")

    return fingerprint_db


# 保存指纹数据库到 JSON 文件
def save_fingerprint_db(fingerprint_db, filename="generate_fingerprint_db.json"):
    with open(filename, 'w') as f:
        json.dump(fingerprint_db, f, indent=4)
    print(f"指纹数据库已保存到文件：{filename}")


# 主函数
if __name__ == "__main__":
    print("开始 WiFi 指纹数据采集...")
    fingerprint_db = collect_fingerprint_data()
    save_fingerprint_db(fingerprint_db)
