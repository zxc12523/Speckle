#!/bin/bash


compileFlag='--compile'
runFlag='--run'
isa='riscv'
spec='433.milc'
spec_name='milc'
vlen='128'
plugin='hotblocks'

./gen_binaries.sh ${compileFlag} ${runFlag} --spec ${spec} --isa ${isa} --vlen ${vlen} --plugin ${plugin} --outdir /home/jerry/Speckle/result/${isa}+${vlen}_${spec}_O3
cp /home/jerry/Speckle/build/${spec}_test/${spec_name}_base.${isa} /home/jerry/Speckle/result/${isa}+${vlen}_${spec}_O3

sed -i 's/O3/O3 -fno-vectorize/g' ${isa}.cfg
./gen_binaries.sh ${compileFlag} ${runFlag} --spec ${spec} --isa ${isa} --vlen ${vlen} --plugin ${plugin} --outdir /home/jerry/Speckle/result/${isa}+${vlen}_${spec}_O3_Nloop
cp /home/jerry/Speckle/build/${spec}_test/${spec_name}_base.${isa} /home/jerry/Speckle/result/${isa}+${vlen}_${spec}_O3_Nloop

sed -i 's/O3/O3 -fno-slp-vectorize/g' ${isa}.cfg
./gen_binaries.sh ${compileFlag} ${runFlag} --spec ${spec} --isa ${isa} --vlen ${vlen} --plugin ${plugin} --outdir /home/jerry/Speckle/result/${isa}+${vlen}_${spec}_O3_Nslp_Nloop
cp /home/jerry/Speckle/build/${spec}_test/${spec_name}_base.${isa} /home/jerry/Speckle/result/${isa}+${vlen}_${spec}_O3_Nslp_Nloop

sed -i 's/ -fno-vectorize//g' ${isa}.cfg
./gen_binaries.sh ${compileFlag} ${runFlag} --spec ${spec} --isa ${isa} --vlen ${vlen} --plugin ${plugin} --outdir /home/jerry/Speckle/result/${isa}+${vlen}_${spec}_O3_Nslp
cp /home/jerry/Speckle/build/${spec}_test/${spec_name}_base.${isa} /home/jerry/Speckle/result/${isa}+${vlen}_${spec}_O3_Nslp

sed -i 's/ -fno-slp-vectorize//g' ${isa}.cfg

# python3 main.py --spec ${spec} --target ${isa}+${vlen}