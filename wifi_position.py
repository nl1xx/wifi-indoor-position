import pywifi
import time
import json
import numpy as np
import matplotlib.pyplot as plt


# WiFi扫描
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


# 加载指纹数据库
def load_fingerprint_db(filename="fingerprint_db.json"):
    with open(filename, 'r') as f:
        fingerprint_db = json.load(f)
    return fingerprint_db


# 计算RSSI距离 (欧几里得距离)
def calculate_distance(rssi1, rssi2):
    distance = 0
    for ssid in rssi1.keys():
        rssi1_value = rssi1.get(ssid, -100)
        rssi2_value = rssi2.get(ssid, -100)
        distance += (rssi1_value - rssi2_value) ** 2
    return np.sqrt(distance)


# KNN定位算法
def knn_predict(test_rssi, fingerprint_db, k=3):
    distances = []
    for record in fingerprint_db:
        location = record["location"]
        rssis = record["rssis"]
        distance = calculate_distance(test_rssi, rssis)
        distances.append((distance, location))

    # 根据距离由小到大排序, 选择最近的k个参考点
    distances.sort(key=lambda x: x[0])
    nearest_locations = [loc for _, loc in distances[:k]]

    # 计算最近k个位置的平均值
    x = np.mean([loc[0] for loc in nearest_locations])
    y = np.mean([loc[1] for loc in nearest_locations])
    return (x, y), nearest_locations


# 预测位置
def predict_location(fingerprint_db):
    print("正在扫描 WiFi...")
    ap_list = scan_wifi()
    print(f"实时扫描的WiFi RSSI数据：{ap_list}")

    ssids = fingerprint_db[0]["rssis"].keys()
    test_rssi = {}
    for ssid in ssids:
        test_rssi[ssid] = ap_list.get(ssid, -100)
    location, nearest = knn_predict(test_rssi, fingerprint_db)
    return location, nearest


def plot_location(fingerprint_db, predicted_location, nearest_locations):
    plt.figure(figsize=(8, 8))
    # 绘制指纹数据库中的参考点
    for record in fingerprint_db:
        loc = record["location"]
        plt.scatter(loc[0], loc[1], c='blue', s=100, label='Reference Point' if loc == fingerprint_db[0]["location"] else "")

    # 绘制预测位置
    plt.scatter(predicted_location[0], predicted_location[1], c='red', s=200, marker='x', label='Predicted Location')

    # 绘制KNN选取的三个点
    for loc in nearest_locations:
        plt.scatter(loc[0], loc[1], c='yellow', s=150, marker='s', label='Nearest KNN Point' if loc == nearest_locations[0] else "")

    plt.title("WiFi Fingerprinting Location using KNN")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend()
    plt.grid()
    plt.show()


# 主函数
if __name__ == "__main__":
    fingerprint_db = load_fingerprint_db()
    print("加载指纹数据库完成")
    predicted_location, nearest_location = predict_location(fingerprint_db)
    print(f"预测位置: {predicted_location}")
    plot_location(fingerprint_db, predicted_location, nearest_location)
