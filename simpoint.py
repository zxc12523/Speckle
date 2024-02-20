import subprocess
import time

BENCHMARKS=["400.perlbench", "401.bzip2", "403.gcc", "429.mcf", "445.gobmk", 
            "456.hmmer", "458.sjeng", "462.libquantum", "464.h264ref", 
            "471.omnetpp", "473.astar", "483.xalancbmk"]

compileFlag='--compile'
runFlag='--run'
isa='riscv'
spec='433.milc'
spec_name='milc'
vlen='128'
plugin='bbv'
root_dir='/local/jerry'


for b in BENCHMARKS:
    p = subprocess.Popen(["{}/SimPoint/bin/simpoint".format(root_dir), 
                    "-inputVectorsGzipped", 
                    "-loadFVFile", "{}/Speckle/result/{}+{}_{}_O3/trace_bbv.gz".format(root_dir, isa, vlen, b), 
                    "-k", "10", 
                    "-saveSimpoints", "{}/Speckle/result/{}+{}_{}_O3/trace.simpts".format(root_dir, isa, vlen, b), 
                    "-saveSimpointWeights", "{}/Speckle/result/{}+{}_{}_O3/trace.weights".format(root_dir, isa, vlen, b)])


