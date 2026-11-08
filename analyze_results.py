
import csv
from pathlib import Path

experiments = {
    "Baseline": "results/baseline/stats.txt",
    "Larger caches": "results/cache_size/larger/stats.txt",
    "Higher associativity": "results/associativity/higher/stats.txt",
    "128-byte blocks": "results/block_size/128B/stats.txt",
    "128-entry TLB": "results/virtual_memory/tlb128/stats.txt",
}

metrics = {
    "simSeconds": "Simulation time (s)",
    "simInsts": "Instructions",
    "system.cpu.ipc": "IPC",
    "system.l1d.overallHits::total": "L1 data hits",
    "system.l1d.overallMisses::total": "L1 data misses",
    "system.l1d.overallMissRate::total": "L1 data miss rate",
    "system.l2.overallMissRate::total": "L2 miss rate",
}

def read_stats(filename):
    values = {}
    with open(filename, encoding="utf-8") as file:
        for line in file:
            parts = line.split()
            if len(parts) >= 2 and parts[0] in metrics:
                values[parts[0]] = float(parts[1])
    return values

rows = []

for name, filename in experiments.items():
    stats = read_stats(filename)
    row = {"Configuration": name}
    for key, label in metrics.items():
        row[label] = stats.get(key)
    rows.append(row)

output = Path("results/comparison.csv")

with output.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["Configuration"] + list(metrics.values())
    )
    writer.writeheader()
    writer.writerows(rows)

print("Comparison table saved:", output)
for row in rows:
    print(
        row["Configuration"],
        "IPC:", row["IPC"],
        "L1 miss rate:", row["L1 data miss rate"]
    )

try:
    import matplotlib.pyplot as plt

    names = [row["Configuration"] for row in rows]
    ipc = [row["IPC"] for row in rows]
    misses = [
        row["L1 data miss rate"] * 100 for row in rows
    ]

    plt.figure(figsize=(10, 5))
    plt.bar(names, ipc)
    plt.ylabel("Instructions per Cycle")
    plt.title("gem5 CPU Performance Comparison")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig("results/ipc_comparison.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 5))
    plt.bar(names, misses)
    plt.ylabel("L1 Data Cache Miss Rate (%)")
    plt.title("gem5 Cache Miss Rate Comparison")
    plt.xticks(rotation=20, ha="right")
    plt.tight_layout()
    plt.savefig("results/cache_miss_comparison.png", dpi=200)
    plt.close()

    print("Graphs generated successfully.")

except ImportError:
    print("Matplotlib is not installed.")
    print("CSV table was still generated successfully.")
