from pathlib import Path
import timeit
import csv
import platform

from matplotlib.colors import ListedColormap
import matplotlib.pyplot as plt


from perf_data import versions
from perf_data.categoies import categories


def plot_mesures_bar(
    plot_results: dict[str, list[float]],
    output_file: str = "performance_comparison.png",
    folder: Path = None,
    title: str = None,
):

    plt.figure(figsize=(12, 8))

    x = [i[0].title() for i in plot_results.items()]
    y = [i[1][0] for i in plot_results.items()]

    palette = ListedColormap(plt.get_cmap("Set2").colors)
    num_colors = len(palette.colors)
    colors = [palette(i % num_colors) for i in range(len(x))]

    plt.bar(x, y, color=colors)

    plt.title(", ".join(["Performance Comparison of Different Versions", title]))
    plt.xlabel("Version")
    plt.ylabel("Average Time (seconds)")
    plt.grid(True)
    # plt.legend()
    plt.tight_layout()
    if folder:
        folder.mkdir(parents=True, exist_ok=True)
        output_file = str(folder / output_file)
    plt.savefig(output_file, dpi=300)
    print(f"Saved results to: {output_file}")


def plot_mesures(
    plot_results: dict[str, list[float]],
    output_file: str = "performance_comparison.png",
    folder: Path = None,
):
    plt.figure(figsize=(12, 8))
    markers = [
        "o",
        "s",
        "D",
        "^",
        "v",
        "<",
        ">",
        "p",
        "h",
        "H",
        "x",
        "X",
        "d",
        "|",
        "_",
    ]
    for i, fun_name in enumerate(plot_results):
        plt.plot(
            categories.keys(),
            plot_results[fun_name],
            marker=markers[i % len(markers)],
            label=fun_name.title(),
        )

    plt.title("Performance Comparison of Different Versions")
    plt.xlabel("Category")
    plt.ylabel("Average Time (seconds)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    if folder:
        folder.mkdir(parents=True, exist_ok=True)
        output_file = str(folder / output_file)
    plt.savefig(output_file, dpi=300)
    print(f"Saved results to: {output_file}")


def save_csv(
    plot_results: dict,
    output_file: str = "performance_comparison.csv",
    folder: Path = None,
):
    if folder:
        folder.mkdir(parents=True, exist_ok=True)
        output_file = str(folder / output_file)
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Version"] + list(categories.keys()))
        for category, version in plot_results.items():
            writer.writerow([category] + version)
    print(f"Saved results to: {output_file}")


## MAIN

functions_list = [
    (lambda: versions.version_1(test_str), "Version 1"),
    (lambda: versions.version_2(test_str), "Version 2"),
    (lambda: versions.version_3(test_str), "Version 3"),
    (lambda: versions.version_4(test_str), "Version 4"),
    (lambda: versions.version_5(test_str), "Version 5"),
    (lambda: versions.version_6(test_str), "Version 6"),
]


times = 5_000_000
repeat = 3
# times = 1000
# repeat = 1

python_ver = platform.system() + "_" + platform.python_version()

results_folder = Path(__file__).parent / "results" / python_ver
results_folder.mkdir(parents=True, exist_ok=True)

print(f"{python_ver}, {times=}, {repeat=}")
results = {fun_name: [] for _, fun_name in functions_list}

for cat, test_str in categories.items():
    print(f"\nCategory: '{cat}'")
    for fun, fun_name in functions_list:
        result_version = fun()
        time_version = timeit.repeat(fun, number=times, repeat=repeat)
        avg_time_version = sum(time_version) / len(time_version)
        results[fun_name].append(avg_time_version)
        print(
            f" - {fun_name.title()}. Time: {[f'{t:.4f}' for t in time_version]} "
            f"avg: {avg_time_version:.4f} seconds. Result: {result_version}"
        )

for i, cat in enumerate(categories):
    plot_mesures_bar(
        {k: [v[i]] for k, v in results.items()},
        f"performance_comparison_{cat}.png",
        folder=results_folder,
        title=cat,
    )
plot_mesures(results, folder=results_folder)
save_csv(results, folder=results_folder)
print("Press Enter to exit...")
input()
