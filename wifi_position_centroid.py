import json
import random
import matplotlib.pyplot as plt


def generate_wifi_data(num_positions=10, max_x=100, max_y=100):
    data = []
    for _ in range(num_positions):
        x, y = random.uniform(0, max_x), random.uniform(0, max_y)
        data.append({
            "position": {"x": x, "y": y}
        })
    return data


def save_to_json(data, filename="wifi_data_centroid.json"):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)


def load_from_json(filename="wifi_data_centroid.json"):
    with open(filename, "r") as file:
        return json.load(file)


def calculate_centroid(reference_data):
    sum_x, sum_y = 0, 0
    num_points = len(reference_data)

    for ref_point in reference_data:
        sum_x += ref_point["position"]["x"]
        sum_y += ref_point["position"]["y"]

    centroid_x = sum_x / num_points
    centroid_y = sum_y / num_points
    return {"x": centroid_x, "y": centroid_y}


def visualize(reference_data, centroid):
    plt.figure(figsize=(10, 8))

    for ref_point in reference_data:
        x, y = ref_point["position"]["x"], ref_point["position"]["y"]
        plt.scatter(x, y, c="blue", label="Reference Point" if "Reference Point" not in plt.gca().get_legend_handles_labels()[1] else "", alpha=0.7)
        plt.text(x + 1, y + 1, f"({x:.1f}, {y:.1f})", fontsize=9)

    cent_x, cent_y = centroid["x"], centroid["y"]
    plt.scatter(cent_x, cent_y, c="red", label="Centroid", s=100, edgecolors="black")
    plt.text(cent_x + 1, cent_y + 1, f"({cent_x:.1f}, {cent_y:.1f})", fontsize=10, color="red")

    plt.legend()
    plt.title("WiFi Indoor Positioning - Centroid Algorithm")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    generated_data = generate_wifi_data()
    save_to_json(generated_data)

    loaded_data = load_from_json()

    centroid = calculate_centroid(loaded_data)

    print("Centroid: ", centroid)

    visualize(loaded_data, centroid)
