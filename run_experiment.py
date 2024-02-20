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

processes = []

for b in BENCHMARKS:
    with open("{}/Speckle/result/{}+{}_{}_O3/compile.log".format(root_dir, isa, vlen, b), 'a') as compileLog:
        p = subprocess.Popen(["{}/Speckle/gen_binaries.sh".format(root_dir), 
                        compileFlag,
                        "--spec", b, 
                        "--isa", isa, 
                        "--vlen", vlen, 
                        "--plugin", plugin, 
                        "--outdir", "{}/Speckle/result/{}+{}_{}_O3/".format(root_dir, isa, vlen, b)], 
                        stdout=compileLog, stderr=compileLog)
        
        processes.append(p)

exit_code = [p.wait() for p in processes]

print(exit_code)



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