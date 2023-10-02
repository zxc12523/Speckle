#!/bin/bash

isa='riscv'
spec='fp'

while test $# -gt 0
do
   case "$1" in
        --spec)
            spec=$2
            shift
            ;;
        --isa)
            isa=$2
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

./gen_binaries.sh --compile --run --spec ${spec} --isa ${isa} --outdir /home/jerry/Speckle/result_${isa}_${spec}_O3

sed -i 's/O3/O3 -fno-vectorize/g' ${isa}.cfg
./gen_binaries.sh --compile --run --spec ${spec} --isa ${isa} --outdir /home/jerry/Speckle/result_${isa}_${spec}_O3_Nloop

sed -i 's/O3/O3 -fno-slp-vectorize/g' ${isa}.cfg
./gen_binaries.sh --compile --run --spec ${spec} --isa ${isa} --outdir /home/jerry/Speckle/result_${isa}_${spec}_O3_Nslp_Nloop

sed -i 's/ -fno-vectorize//g' ${isa}.cfg
./gen_binaries.sh --compile --run --spec ${spec} --isa ${isa} --outdir /home/jerry/Speckle/result_${isa}_${spec}_O3_Nslp

sed -i 's/ -fno-slp-vectorize//g' ${isa}.cfg