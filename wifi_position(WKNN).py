import pywifi
import time
import json
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


# 计算权重
def calculate_weights(rssi1, rssi2):
    weights = {}
    total_weight = 0  # 用于计算所有权重的总和
    for ssid in rssi1.keys():
        rssi1_value = rssi1.get(ssid, -100)
        rssi2_value = rssi2.get(ssid, -100)
        weight = 1 / (1 + (rssi1_value - rssi2_value) ** 2)
        weights[ssid] = weight
        total_weight += weight

    for ssid in weights:
        weights[ssid] /= total_weight

    return weights


# 加权KNN
def wknn_predict(test_rssi, fingerprint_db, k=3):
    distances = []
    for record in fingerprint_db:
        location = record["location"]
        rssis = record["rssis"]

        weights = calculate_weights(test_rssi, rssis)

        # 加权距离计算
        weighted_distance = sum(weights[ssid] * (test_rssi[ssid] - rssis[ssid]) ** 2 for ssid in test_rssi)

        distances.append((weighted_distance, location, weights))

    # 根据加权距离由小到大排序
    distances.sort(key=lambda x: x[0])

    # 获取最近的k个位置
    nearest_locations = [loc for _, loc, _ in distances[:k]]

    # 获取最近的k个位置对应的权重
    nearest_weights = [weights for _, _, weights in distances[:k]]

    # 计算加权坐标
    x_sum = 0
    y_sum = 0
    total_weight = 0

    for loc, weights in zip(nearest_locations, nearest_weights):
        weight_sum = sum(weights.values())
        x_sum += loc[0] * weight_sum
        y_sum += loc[1] * weight_sum
        total_weight += weight_sum

    # 计算加权平均坐标
    if total_weight > 0:
        x = x_sum / total_weight
        y = y_sum / total_weight
    else:
        x = 0
        y = 0

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
    location, nearest = wknn_predict(test_rssi, fingerprint_db)
    return location, nearest


def plot_location(fingerprint_db, predicted_location, nearest_locations):
    plt.figure(figsize=(8, 8))
    # 绘制指纹数据库中的参考点
    for record in fingerprint_db:
        loc = record["location"]
        plt.scatter(loc[0], loc[1], c='blue', s=100, label='Reference Point' if loc == fingerprint_db[0]["location"] else "")

    # 绘制预测位置
    plt.scatter(predicted_location[0], predicted_location[1], c='red', s=200, marker='x', label='Predicted Location')

    for loc in nearest_locations:
        plt.scatter(loc[0], loc[1], c='yellow', s=150, marker='s', label='Nearest KNN Point' if loc == nearest_locations[0] else "")

    plt.title("WiFi Fingerprinting Location using KNN")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend()
    plt.grid()
    plt.show()


if __name__ == "__main__":
    fingerprint_db = load_fingerprint_db()
    print("加载指纹数据库完成")
    predicted_location, nearest_location = predict_location(fingerprint_db)
    print(f"预测位置: {predicted_location}")
    plot_location(fingerprint_db, predicted_location, nearest_location)
