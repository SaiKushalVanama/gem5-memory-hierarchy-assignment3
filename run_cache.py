
import argparse
import m5
from m5.objects import *

# Command-line options for cache experiments.
parser = argparse.ArgumentParser()
parser.add_argument("--l1-size", default="16kB")
parser.add_argument("--l1-assoc", type=int, default=2)
parser.add_argument("--l2-size", default="128kB")
parser.add_argument("--l2-assoc", type=int, default=8)
parser.add_argument("--line-size", type=int, default=64)
parser.add_argument("--tlb-size", type=int, default=64)
parser.add_argument("--benchmark", default="memory_benchmark")
args = parser.parse_args()

# Create the simulated system.
system = System()

system.clk_domain = SrcClockDomain()
system.clk_domain.clock = "1GHz"
system.clk_domain.voltage_domain = VoltageDomain()

system.mem_mode = "timing"
system.mem_ranges = [AddrRange("512MB")]
system.cache_line_size = args.line_size

# Create the x86 CPU.
system.cpu = TimingSimpleCPU()
system.cpu.createInterruptController()

# Configure instruction and data TLB capacities.
system.cpu.mmu.itb.size = args.tlb_size
system.cpu.mmu.dtb.size = args.tlb_size

# Create the main memory bus.
system.membus = SystemXBar()

# Connect the x86 interrupt controller.
system.cpu.interrupts[0].pio = system.membus.mem_side_ports
system.cpu.interrupts[0].int_requestor = system.membus.cpu_side_ports
system.cpu.interrupts[0].int_responder = system.membus.mem_side_ports

# L1 instruction cache.
system.l1i = Cache(
    size=args.l1_size,
    assoc=args.l1_assoc,
    tag_latency=2,
    data_latency=2,
    response_latency=2,
    mshrs=4,
    tgts_per_mshr=8
)

# L1 data cache.
system.l1d = Cache(
    size=args.l1_size,
    assoc=args.l1_assoc,
    tag_latency=2,
    data_latency=2,
    response_latency=2,
    mshrs=4,
    tgts_per_mshr=8
)

# Connect the CPU to the L1 caches.
system.cpu.icache_port = system.l1i.cpu_side
system.cpu.dcache_port = system.l1d.cpu_side

# L1-to-L2 interconnect.
system.l2bus = L2XBar()

system.l1i.mem_side = system.l2bus.cpu_side_ports
system.l1d.mem_side = system.l2bus.cpu_side_ports

# Unified L2 cache.
system.l2 = Cache(
    size=args.l2_size,
    assoc=args.l2_assoc,
    tag_latency=10,
    data_latency=10,
    response_latency=10,
    mshrs=16,
    tgts_per_mshr=16
)

system.l2.cpu_side = system.l2bus.mem_side_ports
system.l2.mem_side = system.membus.cpu_side_ports

# Main memory controller.
system.mem_ctrl = MemCtrl()
system.mem_ctrl.dram = DDR3_1600_8x8()
system.mem_ctrl.dram.range = system.mem_ranges[0]
system.mem_ctrl.port = system.membus.mem_side_ports

# Connect the system port.
system.system_port = system.membus.cpu_side_ports

# Configure syscall-emulation workload.
system.workload = SEWorkload.init_compatible(args.benchmark)

process = Process()
process.cmd = [args.benchmark]

system.cpu.workload = process
system.cpu.createThreads()

# Initialize and execute the simulation.
root = Root(full_system=False, system=system)
m5.instantiate()

print("Beginning cache simulation!")
print("L1 size:", args.l1_size)
print("L1 associativity:", args.l1_assoc)
print("L2 size:", args.l2_size)
print("L2 associativity:", args.l2_assoc)
print("Cache line size:", args.line_size)
print("TLB entries:", args.tlb_size)

exit_event = m5.simulate()

print("Simulation completed!")
print("Exit tick:", m5.curTick())
print("Exit reason:", exit_event.getCause())
