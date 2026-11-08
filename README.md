Exploring Memory Hierarchy Design in gem5

Course: Computer Architecture and Design (MSCS-531-B01)
Assignment: Week 3 – Assignment 3
Simulator: gem5 version 25.1.0.0
Environment: Ubuntu 24.04 (WSL2)

Project Overview

This project investigates memory hierarchy performance using the gem5 architectural simulator. The experiments examine the effects of cache capacity, associativity, cache block size, and translation lookaside buffer (TLB) capacity on processor performance.

Experimental Configuration

CPU: TimingSimpleCPU, 1 GHz

Memory: 512 MiB

L1 instruction cache: 16 KiB

L1 data cache: 16 KiB

L2 cache: 128 KiB

Baseline cache block size: 64 bytes

Baseline TLB capacity: 64 entries

Benchmark: 1 MiB array accessed sequentially over 20 iterations

Experiments

Baseline cache configuration

Increased L1 and L2 cache sizes

Increased cache associativity

Increased cache block size to 128 bytes

Increased instruction and data TLB capacities to 128 entries

Results

The 128-byte cache block configuration achieved the highest IPC of 0.261274 and reduced the L1 data-cache miss rate to approximately 1.0862%.

Increasing cache capacity, associativity, and TLB capacity produced negligible performance changes for this workload.

The experiments used syscall-emulation mode. Operating-system page faults and alternative page sizes were not experimentally evaluated.

Reproducing the Experiments

A compatible x86 gem5 installation is required.

Compile the benchmark:

gcc -O0 -static -o memory_benchmark memory_benchmark.c

Run the baseline configuration:

build/X86/gem5.opt --outdir=assignment3/results/baseline \
  assignment3/run_cache.py \
  --benchmark=assignment3/memory_benchmark

Run the TLB experiment:

build/X86/gem5.opt --outdir=assignment3/results/virtual_memory/tlb128 \
  assignment3/run_cache.py \
  --benchmark=assignment3/memory_benchmark \
  --tlb-size=128

These commands assume the repository files are placed inside an assignment3 directory under the gem5 root. Adjust paths for your local installation.

Generate the comparison CSV and graphs by running python3 analyze_results.py from the assignment directory.

Project Files

run_cache.py – gem5 simulation configuration

memory_benchmark.c – memory-access benchmark

analyze_results.py – statistics analysis and graph generation

results/ – experimental configurations, statistics, and graphs

Conclusion

The experiments demonstrate that memory hierarchy performance depends on workload characteristics. Larger cache blocks provided measurable benefits for the sequential-access benchmark, while increasing cache capacity, associativity, and TLB entries did not significantly improve performance.
