#!/bin/bash
#set -e

#############
# TODO
#  * allow the user to input their desired input set
#  * auto-handle output file generation

export SPEC_DIR=../SPEC_CPU2006v1.1

if [ -z  "$SPEC_DIR" ]; then 
   echo "  Please set the SPEC_DIR environment variable to point to your copy of SPEC CPU2006."
   exit 1
fi

# idiomatic parameter and option handling in sh
compileFlag=false
runFlag=false
copyFlag=false
CONFIG="riscv"
SPEC="fp"
vlen='256'
PLUGIN=''
CMD_FILE=commands.txt
INPUT_TYPE=test
OUT_DIR="/home/jerry/Speckle/tmp"

while test $# -gt 0
do
   case "$1" in
        --compile) 
            compileFlag=true
            ;;
        --run) 
            runFlag=true
            ;;
        --copy)
            copyFlag=true
            ;;
        --spec)
            SPEC=$2
            shift
            ;;
        --isa)
            CONFIG=$2
            shift
            ;;
        --vlen)
            vlen=$2
            shift
            ;;
        --outdir)
            OUT_DIR=$2
            shift
            ;;
        --plugin)
            PLUGIN=$2
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

# CONFIG=riscv
# RUN="spike /opt/riscv/riscv64-unknown-linux-gnu/bin/pk "

CONFIGFILE=${CONFIG}.cfg

if [[ ${CONFIG} =~ "arm" ]]; then
   RUN="/opt/riscv/qemu/bin/qemu-aarch64 -cpu max,sve${vlen}=on "
else 
   RUN="/opt/riscv/qemu/bin/qemu-riscv64 -cpu rv64,v=true,vlen=${vlen},vext_spec=v1.0 -L /usr/riscv64-linux-gnu/"
fi

if [[ ${PLUGIN} == 'howvec' ]]; then
   OPTION="-plugin /local/jerry/qemu/build/contrib/plugins/libhowvec.so,inline=on -d plugin"
elif [[ ${PLUGIN} == 'hotblocks' ]]; then
   OPTION="-plugin /local/jerry/qemu/build/contrib/plugins/libhotblocks.so,inline=on -d plugin"
elif [[ ${PLUGIN} == 'bbv' ]]; then
   OPTION="-plugin /local/jerry/qemu/build/contrib/plugins/libbbv.so -d plugin"
elif [[ ${PLUGIN} == 'trace' ]]; then
   OPTION="-plugin /local/jerry/qemu/build/contrib/plugins/libtracer.so -d plugin"
fi

if [[ ${SPEC} == "fp" ]]; then
   BENCHMARKS=(433.milc 444.namd 447.dealII 450.soplex 453.povray 470.lbm 482.sphinx3)
elif [[ ${SPEC} == "int" ]]; then
   BENCHMARKS=(400.perlbench 401.bzip2 403.gcc 429.mcf 445.gobmk 456.hmmer 458.sjeng 462.libquantum 464.h264ref 471.omnetpp 473.astar 483.xalancbmk)
else 
   BENCHMARKS=${SPEC}
fi


echo "== Speckle Options =="
echo "  Spec2006  : " ${SPEC}
echo "  Config    : " ${CONFIG}
echo "  Input     : " ${INPUT_TYPE}
echo "  Output    : " ${OUT_DIR}
echo "  compile   : " $compileFlag
echo "  run       : " $runFlag
echo "  copy      : " $copyFlag
echo "  RUN       : " $RUN
echo "  OPTION    : " $OPTION
echo ""

# echo ${CONFIG%+*}

BUILD_DIR=$PWD/build
COPY_DIR=$PWD/${CONFIG}-spec-${INPUT_TYPE}
mkdir -p build;
mkdir -p ${OUT_DIR}

# compile the binaries
if [ "$compileFlag" = true ]; then
   echo "Compiling SPEC..."
   # copy over the config file we will use to compile the benchmarks
   cp $BUILD_DIR/../${CONFIGFILE} $SPEC_DIR/config/${CONFIGFILE}
   cd $SPEC_DIR; . ./shrc; time runspec --config ${CONFIG} --size ${INPUT_TYPE} --action setup ${BENCHMARKS[@]}
   # cd $SPEC_DIR; . ./shrc; time runspec --config ${CONFIG} --size ${INPUT_TYPE} --action scrub int

   if [ "$copyFlag" = true ]; then
      rm -rf $COPY_DIR
      mkdir -p $COPY_DIR
   fi

   # copy back over the binaries.  Fuck xalancbmk for being different.
   # Do this for each input type.
   # assume the CPU2006 directories are clean. I've hard-coded the directories I'm going to copy out of
   for b in ${BENCHMARKS[@]}; do
      echo ${b}
      SHORT_EXE=${b##*.} # cut off the numbers ###.short_exe
      if [ $b == "483.xalancbmk" ]; then 
         SHORT_EXE=Xalan #WTF SPEC???
      fi
      BMK_DIR=$SPEC_DIR/benchspec/CPU2006/$b/run/run_base_${INPUT_TYPE}_${CONFIG%+*}.0000;
      
      # echo ""
      # echo "ls $SPEC_DIR/benchspec/CPU2006/$b/run"
      # ls $SPEC_DIR/benchspec/CPU2006/$b/run
      # ls $SPEC_DIR/benchspec/CPU2006/$b/run/run_base_${INPUT_TYPE}_${CONFIG}.0000
      # echo ""

      # make a symlink to SPEC (to prevent data duplication for huge input files)
      echo "ln -sf $BMK_DIR $BUILD_DIR/${b}_${INPUT_TYPE}"
      if [ -d $BUILD_DIR/${b}_${INPUT_TYPE} ]; then
         echo "unlink $BUILD_DIR/${b}_${INPUT_TYPE}"
         unlink $BUILD_DIR/${b}_${INPUT_TYPE}
      fi
      ln -sf $BMK_DIR $BUILD_DIR/${b}_${INPUT_TYPE}

      if [ "$copyFlag" = true ]; then
         echo "---- copying benchmarks ----- "
         mkdir -p $COPY_DIR/$b
         cp -r $BUILD_DIR/../commands $COPY_DIR/commands
         cp $BUILD_DIR/../run.sh $COPY_DIR/run.sh
         sed -i '4s/.*/INPUT_TYPE='${INPUT_TYPE}' #this line was auto-generated from gen_binaries.sh/' $COPY_DIR/run.sh
         for f in $BMK_DIR/*; do
            echo $f
            if [[ -d $f ]]; then
               cp -r $f $COPY_DIR/$b/$(basename "$f")
            else
               cp $f $COPY_DIR/$b/$(basename "$f")
            fi
         done
         mv $COPY_DIR/$b/${SHORT_EXE}_base.${CONFIG} $COPY_DIR/$b/${SHORT_EXE}
      fi
   done
fi

# running the binaries/building the command file
# we could also just run through BUILD_DIR/CMD_FILE and run those...
if [ "$runFlag" = true ]; then

   for b in ${BENCHMARKS[@]}; do
   
      cd $BUILD_DIR/${b}_${INPUT_TYPE}
      SHORT_EXE=${b##*.} # cut off the numbers ###.short_exe
      # handle benchmarks that don't conform to the naming convention
      if [ $b == "482.sphinx3" ]; then SHORT_EXE=sphinx_livepretend; fi
      if [ $b == "483.xalancbmk" ]; then SHORT_EXE=Xalan; fi
      
      # read the command file
      IFS=$'\n' read -d '' -r -a commands < $BUILD_DIR/../commands/${b}.${INPUT_TYPE}.cmd

      for input in "${commands[@]}"; do
         if [[ ${input:0:1} != '#' ]]; then # allow us to comment out lines in the cmd files

            if [[ ${PLUGIN} == 'trace' ||  ${PLUGIN} == 'bbv' ]]; then

               echo "cp \"${OUT_DIR}trace*\" ."
               cp ${OUT_DIR}trace* .
            fi

            echo "~~~Running ${b}" 
            echo "  ${RUN} ${OPTION} ${SHORT_EXE}_base.${CONFIG} ${input}"
            eval ${RUN} ${OPTION} ${SHORT_EXE}_base.${CONFIG%+*} ${input} > /dev/null 2> ${OUT_DIR}/result.log
            
            if [[ ${PLUGIN} == 'trace' || ${PLUGIN} == 'bbv' ]]; then
               mv trace* ${OUT_DIR}
            fi
         fi
      done
   
   done

fi

echo ""
echo "Done!"
