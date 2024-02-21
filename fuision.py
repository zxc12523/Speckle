import subprocess
import time
import os

BENCHMARKS=["400.perlbench", "401.bzip2", "403.gcc", "429.mcf", "445.gobmk", 
            "456.hmmer", "458.sjeng", "462.libquantum", "464.h264ref", 
            "471.omnetpp", "473.astar", "483.xalancbmk"]

# BENCHMARKS=["401.bzip2"]

compileFlag='--compile'
runFlag='--run'
isa='riscv'
vlen='128'
plugin='trace'
root_dir='/local/jerry'

processes = []

os.chdir("{}/riscv-perf-model/build".format(root_dir))

for b in BENCHMARKS:
    for i in range(10):
        with open("/dev/null", 'w') as nullfile, open("{}/Speckle/result/riscv+128_{}_O3/fusion{}.txt".format(root_dir, b, i), 'w') as outfile:
            p = subprocess.Popen(["./olympia", "-i10M", "--arch", "big_core", "{}/Speckle/result/riscv+128_{}_O3/trace{}.txt".format(root_dir, b, i)] , stdout=nullfile, stderr=outfile)
    
        processes.append(p)

    exit_code = [p.wait() for p in processes]

    print(exit_code)

    processes.clear()



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