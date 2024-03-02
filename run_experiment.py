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
plugin='bbv'
root_dir='/local/jerry'

start =  time.time()

print("Generating basic block vector...")

processes = []

for b in BENCHMARKS:
    if not os.path.exists("{}/Speckle/result/{}+{}_{}_O3/{}/".format(root_dir, isa, vlen, b, plugin)): 
        os.makedirs("{}/Speckle/result/{}+{}_{}_O3/{}/".format(root_dir, isa, vlen, b, plugin)) 

    with open("{}/Speckle/result/{}+{}_{}_O3/{}/execution.log".format(root_dir, isa, vlen, plugin, b), 'a') as executionLog:
        p = subprocess.Popen(["{}/Speckle/gen_binaries.sh".format(root_dir), 
                        runFlag,
                        "--spec", b, 
                        "--isa", isa, 
                        "--vlen", vlen, 
                        "--plugin", 'bbv', 
                        "--outdir", "{}/Speckle/result/{}+{}_{}_O3/{}/".format(root_dir, isa, vlen, b, plugin)], 
                        stdout=executionLog, stderr=executionLog)
        
        processes.append(p)

exit_code = [p.wait() for p in processes]

print(time.time() - start, exit_code)

print("Generating simpoints...")

processes = []

for b in BENCHMARKS:
    p = subprocess.Popen(["{}/SimPoint/bin/simpoint".format(root_dir), 
                    "-inputVectorsGzipped", 
                    "-loadFVFile", "{}/Speckle/result/{}+{}_{}_O3/{}/trace_bbv.gz".format(root_dir, isa, vlen, b), 
                    "-k", "10", 
                    "-saveSimpoints", "{}/Speckle/result/{}+{}_{}_O3/{}/trace.simpts".format(root_dir, isa, vlen, b), 
                    "-saveSimpointWeights", "{}/Speckle/result/{}+{}_{}_O3/{}/trace.weights".format(root_dir, isa, vlen, b)])
    processes.append(p)

exit_code = [p.wait() for p in processes]

print(time.time() - start, exit_code)

print("Generating trace txt...")

processes = []

for b in BENCHMARKS:
    with open("{}/Speckle/result/{}+{}_{}_O3/{}/execution.log".format(root_dir, isa, vlen, b), 'a') as executionLog:
        p = subprocess.Popen(["{}/Speckle/gen_binaries.sh".format(root_dir), 
                        runFlag,
                        "--spec", b, 
                        "--isa", isa, 
                        "--vlen", vlen, 
                        "--plugin", "trace", 
                        "--outdir", "{}/Speckle/result/{}+{}_{}_O3/{}/".format(root_dir, isa, vlen, b)], 
                        stdout=executionLog, stderr=executionLog)
        
        processes.append(p)


exit_code = [p.wait() for p in processes]

print(time.time() - start, exit_code)

print("Generating fusion txt...")

processes = []

os.chdir("{}/riscv-perf-model/release".format(root_dir))

for b in BENCHMARKS:
    for i in range(10):
        with open("/dev/null", 'w') as nullfile, open("{}/Speckle/result/{}+{}_{}_O3/{}/fusion{}.txt".format(root_dir, isa, vlen, b, i), 'w') as outfile:
            p = subprocess.Popen(["./olympia", "-i99M", "--arch", "big_core", "{}/Speckle/result/{}+{}_{}_O3/{}/trace{}.txt".format(root_dir, b, i)] , stdout=nullfile, stderr=outfile)
    
        processes.append(p)

    exit_code = [p.wait() for p in processes]

    print(time.time() - start, exit_code)

    processes.clear()

import numpy as np

for b in BENCHMARKS:
    weight_file = open("{}/Speckle/result/{}+{}_{}_O3/{}/trace.weights".format(root_dir, isa, vlen, b))
    result_file = open("{}/Speckle/result/{}+{}_{}_O3/{}/fusion.result".format(root_dir, isa, vlen, b), "w")

    fusion = []
    weight = [float(s.split(' ')[0]) for s in weight_file.readlines()]


    for i in range(len(weight)):
        fusion_file = open("{}/Speckle/result/{}+{}_{}_O3/{}/fusion{}.txt".format(root_dir, isa, vlen, b, i))
        fusion.append(list(map(int, fusion_file.readline().split(' ')[1:-1])))
        fusion_file.close()
    
    fusion = np.array(fusion, dtype=np.float64)
    weight = np.array(weight)
    
    for i in range(len(weight)):
        fusion[i] *= weight[i]
        fusion[i] /= 99000000
    
    fusion = fusion.sum(axis=0).tolist()
    
    print(fusion)

    result_file.write(str(fusion))
    


    
    


# cp /home/jerry/Speckle/build/${spec}_test/${spec_name}_base.${isa} /home/jerry/Speckle/result/${isa}+${vlen}_${spec}_O3

# sed -i 's/O3/O3 -fno-vectorize/g' ${isa}.cfg
# ./gen_binaries.sh ${compileFlag} ${runFlag} --spec ${spec} --isa ${isa} --vlen ${vlen} --plugin ${plugin} --outdir /home/jerry/Speckle/result/${isa}+${vlen}_${spec}_O3_Nloop
# cp /home/jerry/Speckle/build/${spec}_test/${spec_name}_base.${isa} /home/jerry/Speckle/result/${isa}+${vlen}_${spec}_O3_Nloop

# sed -i 's/O3/O3 -fno-slp-vectorize/g' ${isa}.cfg
# ./gen_binaries.sh ${compileFlag} ${runFlag} --spec ${spec} --isa ${isa} --vlen ${vlen} --plugin ${plugin} --outdir /home/jerry/Speckle/result/${isa}+${vlen}_${spec}_O3_Nslp_Nloop
# cp /home/jerry/Speckle/build/${spec}_test/${spec_name}_base.${isa} /home/jerry/Speckle/result/${isa}+${vlen}_${spec}_O3_Nslp_Nloop

# sed -i 's/ -fno-vectorize//g' ${isa}.cfg
# ./gen_binaries.sh ${compileFlag} ${runFlag} --spec ${spec} --isa ${isa} --vlen ${vlen} --plugin ${plugin} --outdir /home/jerry/Speckle/result/${isa}+${vlen}_${spec}_O3_Nslp
# cp /home/jerry/Speckle/build/${spec}_test/${spec_name}_base.${isa} /home/jerry/Speckle/result/${isa}+${vlen}_${spec}_O3_Nslp

# sed -i 's/ -fno-slp-vectorize//g' ${isa}.cfg

# python3 main.py --spec ${spec} --target ${isa}+${vlen}