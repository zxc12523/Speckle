#!/bin/bash

info=()

while read line
do
    TMP=($(IFS="," echo "$line"))
    # echo ${TMP[0]%,}
    # echo ${TMP[1]%,}
    # echo ${TMP[2]%,}
    # echo ${TMP[3]%,}
    tmp=$(/home/jerry/llvm-project/aarch64/bin/llvm-addr2line -Cfi -e /home/jerry/spec2006/SPEC_CPU2006v1.1.cp/benchspec/CPU2006/464.h264ref/exe/h264ref_base.riscv ${TMP[0]%,})
    # tmp=($(IFS=" " echo "$tmp"))
    # echo ${tmp[@]}
    info[${#info[@]}]=${tmp}
done < "${1:-/dev/stdin}"

for i in ${info[@]}
do 
    echo $i
done

# /home/jerry/llvm-project/riscv/bin/llvm-objdump -d -S /home/jerry/spec2006/SPEC_CPU2006v1.1.cp/benchspec/CPU2006/464.h264ref/exe/h264ref_base.riscv  | grep -A1 -B
# /home/jerry/llvm-project/aarch64/bin/llvm-addr2line -Cfi -e /home/jerry/spec2006/SPEC_CPU2006v1.1.cp/benchspec/CPU2006/464.h264ref/exe/h264ref_base.riscv 