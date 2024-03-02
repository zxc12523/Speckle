import subprocess
import time
import os

# BENCHMARKS=["400.perlbench", "401.bzip2", "403.gcc", "429.mcf", "445.gobmk", 
#             "456.hmmer", "458.sjeng", "462.libquantum", "464.h264ref", 
#             "471.omnetpp", "473.astar", "483.xalancbmk"]

# BENCHMARKS=["445.gobmk"]

BENCHMARKS=["401.bzip2"]

compileFlag='--compile'
runFlag='--run'
isa='riscv'
vlen='128'
plugin='hotblocks'
root_dir='/local/jerry'

start =  time.time()

print("Generating basic block vector...")

processes = []

for b in BENCHMARKS:
    if not os.path.exists("{}/Speckle/result/{}+{}_{}_O3/{}/".format(root_dir, isa, vlen, b, plugin)): 
        os.makedirs("{}/Speckle/result/{}+{}_{}_O3/{}/".format(root_dir, isa, vlen, b, plugin)) 

    with open("{}/Speckle/result/{}+{}_{}_O3/{}/execution.log".format(root_dir, isa, vlen, plugin, b), 'a') as executionLog:
        p = subprocess.Popen(["{}/Speckle/gen_binaries.sh".format(root_dir), 
                        compileFlag,
                        runFlag,
                        "--spec", b, 
                        "--isa", isa, 
                        "--vlen", vlen, 
                        "--plugin", plugin, 
                        "--outdir", "{}/Speckle/result/{}+{}_{}_O3/{}/".format(root_dir, isa, vlen, b, plugin)], 
                        stdout=executionLog, stderr=executionLog)
        
        processes.append(p)

exit_code = [p.wait() for p in processes]

print(time.time() - start, exit_code)