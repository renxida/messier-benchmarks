
# Automatically generated SST Python input
import sst
# from mhlib import componentlist

DEBUG_L1 = 0
DEBUG_L2 = 0
DEBUG_L3 = 0
DEBUG_DIR = 0
DEBUG_MEM = 0

N_NODES = 55

# create memory and net

comp_chiprtr = sst.Component("chiprtr", "merlin.hr_router")
comp_chiprtr.addParams({
    "xbar_bw": "1GB/s",
    "link_bw": "1GB/s",
    "input_buf_size": "1KB",
    "num_ports": N_NODES+1,
    "flit_size": "72B",
    "output_buf_size": "1KB",
    "id": "0",
    "topology": "merlin.singlerouter"
})
comp_chiprtr.setSubComponent("topology", "merlin.singlerouter")

comp_dirctrl = sst.Component("dirctrl", "memHierarchy.DirectoryController")
comp_dirctrl.addParams({
    "coherence_protocol": "MSI",
    "debug": DEBUG_DIR,
    "debug_level": "10",
    "entry_cache_size": "16384",
    "addr_range_end": "0x1F000000",
    "addr_range_start": "0x0",
    "verbose": 2,
})
dirNIC = comp_dirctrl.setSubComponent("cpulink", "memHierarchy.MemNIC")
dirNIC.addParams({
    "network_bw": "25GB/s",
    "group": 2,
    "verbose": 2,
    # "debug" : 1,
    # "debug_level" : 10,
})
dirMemLink = comp_dirctrl.setSubComponent(
    "memlink", "memHierarchy.MemLink")  # Not on a network, just a direct link

memctrl = sst.Component("memory", "memHierarchy.MemController")
memctrl.addParams({
    "debug": DEBUG_MEM,
    "debug_level": 10,
    "clock": "1GHz",
    "verbose": 2,
})
memToDir = memctrl.setSubComponent("cpulink", "memHierarchy.MemLink")




# set bakcned to messier
nvm_memory_backend = memctrl.setSubComponent("backend", "memHierarchy.Messier")

nvm_mem_params = {
    "clock" : "1024 MHz",
    "backing" : "none",
}
nvm_backend_params = {
   # "max_requests_per_cycle" : 1,
    "mem_size" : f"512MiB", 
    #"backendConvertor.backend.clock" : "1024 MHz",
    #"backendConvertor" : "memHierarchy.MemBackendConvertor", 
   # "backend.device_count" : 1,
   # "backend.link_count" : 4,
   # "backend.vault_count" : 16,
   # "backend.queue_depth" : 64,
   # "backend.bank_count" : 16,
   # "backend.dram_count" : 20,
   # "backend.capacity_per_device" : 4, # Min is now 4 but we'll just use 1 of it
   # "backend.xbar_depth" : 128,
   # "backend.max_req_size" : 64,
   # "backend.tag_count" : 512,
}

memctrl.addParams(nvm_mem_params)
nvm_memory_backend.addParams(nvm_backend_params)

messier_inst = sst.Component("NVMmemory", "Messier")

messier_params = {
	"clock" : "1 GHz",

}
messier_inst.addParams(messier_params)

messier_inst.addParams({
      "tCL" : "30",
      "tRCD" : "300",
      "clock" : "1GHz",
      "tCL_W" : "1000",
      "write_buffer_size" : "32",
      "flush_th" : "90",
      "num_banks" : "32",
      "max_outstanding" : "32",
      "max_current_weight" : "160",
      "read_weight" : "5",
      "write_weight" : "50",
      "max_writes" : 4
})


#nvm_memory.addParams({
 #     "coherence_protocol" : "MESI",
#      "backend.access_time" : "1000 ns",
 #     "backend.mem_size" : str(memory_mb * 1024 * 1024) + "B",
#      "clock" : "1GHz"
#})

#nvm_memory.addParams(nvm_mem_params)

link_nvm_bus_link = sst.Link("link_nvm_bus_link")
link_nvm_bus_link.connect( (messier_inst, "bus", "50ps"), (nvm_memory_backend, "nvm_link", "50ps") )


# end messier backend





link_dir_net = sst.Link("link_dir_net")
link_dir_net.connect((comp_chiprtr, "port0", "2000ps"),
                    (dirNIC, "port", "2000ps"))

link_dir_mem = sst.Link("link_dir_mem")
link_dir_mem.connect((dirMemLink, "port", "10000ps"),
                    (memToDir, "port", "10000ps"))

# add nodes using memory and net

for ix in range(N_NODES):
    # Define the simulation components
    comp_cpu = sst.Component(f"cpu_{ix}", "memHierarchy.trivialCPU")
    comp_cpu.addParams({
        "memSize": "0x100000",
        "num_loadstore": "10000",
        "commFreq": "100",
        "do_write": "1"
    })
    iface = comp_cpu.setSubComponent("memory", "memHierarchy.memInterface")

    comp_l1cache = sst.Component(f"l1cache_{ix}", "memHierarchy.Cache")
    comp_l1cache.addParams({
        "access_latency_cycles": "5",
        "cache_frequency": "2 Ghz",
        "replacement_policy": "lru",
        "coherence_protocol": "MSI",
        "associativity": "4",
        "cache_line_size": "64",
        "cache_size": "4 KB",
        "L1": "1",
        "debug": DEBUG_L1,
        "debug_level": 10,
        "verbose": 2,
    })
    l1ToC = comp_l1cache.setSubComponent("cpulink", "memHierarchy.MemLink")
    l1Tol2 = comp_l1cache.setSubComponent("memlink", "memHierarchy.MemLink")

    comp_l2cache = sst.Component(f"l2cache_{ix}", "memHierarchy.Cache")
    comp_l2cache.addParams({
        "access_latency_cycles": "20",
        "cache_frequency": "2 Ghz",
        "replacement_policy": "lru",
        "coherence_protocol": "MSI",
        "associativity": "8",
        "cache_line_size": "64",
        "cache_size": "32 KB",
        "debug": DEBUG_L2,
        "debug_level": 10,
        "verbose": 2,
    })
    l2Tol1 = comp_l2cache.setSubComponent("cpulink", "memHierarchy.MemLink")
    l2Tol3 = comp_l2cache.setSubComponent("memlink", "memHierarchy.MemLink")

    l3cache = sst.Component(f"l3cache_{ix}", "memHierarchy.Cache")
    l3cache.addParams({
        "access_latency_cycles": "100",
        "cache_frequency": "2 Ghz",
        "replacement_policy": "lru",
        "coherence_protocol": "MSI",
        "associativity": "16",
        "cache_line_size": "64",
        "cache_size": "64 KB",
        "debug": DEBUG_L3,
        "debug_level": 10,
        "verbose": 2,
    })
    l3Tol2 = l3cache.setSubComponent("cpulink", "memHierarchy.MemLink")
    l3NIC = l3cache.setSubComponent("memlink", "memHierarchy.MemNIC")
    l3NIC.addParams({
        # "debug" : 1,
        # "debug_level" : 10,
        "network_bw": "25GB/s",
        "group": 1,
        "verbose": 2,
    })

    # Define the simulation links
    link_cpu_l1cache = sst.Link(f"link_cpu_l1cache_{ix}")
    link_cpu_l1cache.connect((iface, "port", "1000ps"), (l1ToC, "port", "1000ps"))

    link_l1cache_l2cache = sst.Link(f"link_l1cache_l2cache_{ix}")
    link_l1cache_l2cache.connect(
        (l1Tol2, "port", "10000ps"), (l2Tol1, "port", "10000ps"))

    link_l2cache_l3cache = sst.Link(f"link_l2cache_l3cache{ix}")
    link_l2cache_l3cache.connect(
        (l2Tol3, "port", "10000ps"), (l3Tol2, "port", "10000ps"))

    link_cache_net = sst.Link(f"link_cache_net_{ix}")
    link_cache_net.connect((l3NIC, "port", "10000ps"),
                        (comp_chiprtr, f"port{ix+1}", "2000ps"))

    


# Enable statistics
sst.setStatisticLoadLevel(7)
sst.setStatisticOutput("sst.statOutputConsole")
# for a in componentlist:
#     sst.enableAllStatisticsForComponentType(a)

# Define the simulation 