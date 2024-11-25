import json
import matplotlib.pyplot as plt


def load_from_json(filename="fingerprint_db.json"):
    with open(filename, 'r') as f:
        return json.load(f)


def generate_Pi():
    pi = []
    dataset = load_from_json()
    for i in range(10):
        rssis_values = list(dataset[i]['rssis'].values())
        length = len(rssis_values)
        if length > 0:
            average_rssi = sum(rssis_values) / length
            p_i = 10 ** (average_rssi / 10)
            pi.append(p_i)
    return pi


def get_position():
    x = []
    y = []
    data = load_from_json("wifi_data_centroid.json")
    for i in range(len(data)):
        position = data[i]['position']
        x.append(position['x'])
        y.append(position['y'])
    return x, y


def p_with_beta(beta=2):
    pi = generate_Pi()
    pi_beta = []
    for i in range(10):
        pi_beta.append(pi[i] ** (1/beta))
    return pi_beta


def calculate_wighted_centroid():
    pi_beta = p_with_beta()
    x, y = get_position()
    a = b = 0
    c = d = 0
    for i in range(len(x)):
        a += pi_beta[i] * x[i]
        b += pi_beta[i]

    for i in range(len(y)):
        c += pi_beta[i] * y[i]
        d += pi_beta[i]
    return a / b, c / d


def visualize():
    data = load_from_json("wifi_data_centroid.json")
    for ref_point in data:
        x, y = ref_point["position"]["x"], ref_point["position"]["y"]
        plt.scatter(x, y, c="blue", label="Reference Point" if "Reference Point" not in plt.gca().get_legend_handles_labels()[1] else "", alpha=0.7)
        plt.text(x + 1, y + 1, f"({x:.1f}, {y:.1f})", fontsize=7)

    predict_x, predict_y = calculate_wighted_centroid()
    plt.scatter(predict_x, predict_y, c="red", label="Centroid", s=100, edgecolors="black")

    plt.legend()
    plt.title("WiFi Indoor Positioning - Centroid Algorithm")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    print(calculate_wighted_centroid())
    visualize()
