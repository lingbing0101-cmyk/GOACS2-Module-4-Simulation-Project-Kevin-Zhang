from bokeh.plotting import figure, output_file, save
from bokeh.layouts import column
from bokeh.models import ColumnDataSource

files = {
    "Simulation 1": "sim1_data.txt",
    "Simulation 2": "sim2_data.txt",
    "Simulation 3": "sim3_data.txt"
}

colors = ["blue", "red", "green"]

p = figure(
    title="Virus Infection Simulation Results",
    x_axis_label="Time to infect all cells (seconds)",
    y_axis_label="Number of trials",
    width=900,
    height=550
)

all_data = []

for label, filename in files.items():
    try:
        with open(filename, "r") as f:
            data = [float(line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        data = []

    if not data:
        print(label, "has no data yet.")
        continue

    all_data.append(data)

if not all_data:
    raise SystemExit("No data found. Run the simulations first.")

minimum = min(min(data) for data in all_data)
maximum = max(max(data) for data in all_data)

if minimum == maximum:
    maximum += 1

bin_count = 15
bin_width = (maximum - minimum) / bin_count

for (label, filename), color in zip(files.items(), colors):
    try:
        with open(filename, "r") as f:
            data = [float(line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        continue

    if not data:
        continue

    bins = [0] * bin_count

    for value in data:
        index = int((value - minimum) / bin_width)
        index = min(index, bin_count - 1)
        bins[index] += 1

    left = [
        minimum + i * bin_width
        for i in range(bin_count)
    ]

    right = [
        minimum + (i + 1) * bin_width
        for i in range(bin_count)
    ]

    source = ColumnDataSource(data={
        "left": left,
        "right": right,
        "top": bins
    })

    p.quad(
        left="left",
        right="right",
        bottom=0,
        top="top",
        source=source,
        color=color,
        alpha=0.35,
        legend_label=f"{label} (n={len(data)})"
    )

p.legend.location = "top_right"
p.legend.click_policy = "hide"

output_file("simdataviz.html")
save(column(p))

print("Visualization created: simdataviz.html")
