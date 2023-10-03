#!/bin/bash


compileFlag=''
runFlag=''
isa='riscv'
spec='fp'
vlen='256'

while test $# -gt 0
do
   case "$1" in
        --compile) 
            compileFlag='--compile'
            ;;
        --run) 
            runFlag='--run'
            ;;
        --spec)
            spec=$2
            shift
            ;;
        --isa)
            isa=$2
            shift
            ;;
        --vlen)
            vlen=$2
            shift
            ;;
        --*) echo "ERROR: bad option $1"
            echo "  --compile (compile the SPEC benchmarks), --run (to run the benchmarks) --copy (copies, not symlinks, benchmarks to a new dir)"
            exit 1
            ;;
        *) echo "ERROR: bad argument $1"
            echo "  --compile (compile the SPEC benchmarks), --run (to run the benchmarks) --copy (copies, not symlinks, benchmarks to a new dir)"
            exit 2
            ;;
    esac
    shift
done

./gen_binaries.sh ${compileFlag} ${runFlag} --spec ${spec} --isa ${isa} --vlen ${vlen} --outdir /home/jerry/Speckle/result/${isa}_${spec}_O3

sed -i 's/O3/O3 -fno-vectorize/g' ${isa}.cfg
./gen_binaries.sh ${compileFlag} ${runFlag} --spec ${spec} --isa ${isa} --vlen ${vlen} --outdir /home/jerry/Speckle/result/${isa}_${spec}_O3_Nloop

sed -i 's/O3/O3 -fno-slp-vectorize/g' ${isa}.cfg
./gen_binaries.sh ${compileFlag} ${runFlag} --spec ${spec} --isa ${isa} --vlen ${vlen} --outdir /home/jerry/Speckle/result/${isa}_${spec}_O3_Nslp_Nloop

sed -i 's/ -fno-vectorize//g' ${isa}.cfg
./gen_binaries.sh ${compileFlag} ${runFlag} --spec ${spec} --isa ${isa} --vlen ${vlen} --outdir /home/jerry/Speckle/result/${isa}_${spec}_O3_Nslp

sed -i 's/ -fno-slp-vectorize//g' ${isa}.cfg