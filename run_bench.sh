echo - 400.perlbench
cd /home/jerry/spec2006/Speckle/build/400.perlbench_test
time ./perlbench_base.riscv -I. -I./lib attrs.pl 1> /dev/null
echo - 400.perlbench
cd /home/jerry/spec2006/Speckle/build/400.perlbench_test
time ./perlbench_base.riscv -I. -I./lib gv.pl 1> /dev/null
echo - 400.perlbench
cd /home/jerry/spec2006/Speckle/build/400.perlbench_test
time ./perlbench_base.riscv -I. -I./lib makerand.pl 1> /dev/null
echo - 400.perlbench
cd /home/jerry/spec2006/Speckle/build/400.perlbench_test
time ./perlbench_base.riscv -I. -I./lib pack.pl 1> /dev/null
echo - 400.perlbench
cd /home/jerry/spec2006/Speckle/build/400.perlbench_test
time ./perlbench_base.riscv -I. -I./lib redef.pl 1> /dev/null
echo - 400.perlbench
cd /home/jerry/spec2006/Speckle/build/400.perlbench_test
time ./perlbench_base.riscv -I. -I./lib ref.pl 1> /dev/null
echo - 400.perlbench
cd /home/jerry/spec2006/Speckle/build/400.perlbench_test
time ./perlbench_base.riscv -I. -I./lib regmesg.pl 1> /dev/null
echo - 400.perlbench
cd /home/jerry/spec2006/Speckle/build/400.perlbench_test
time ./perlbench_base.riscv -I. -I./lib test.pl 1> /dev/null
echo - 401.bzip2
cd /home/jerry/spec2006/Speckle/build/401.bzip2_test
time ./bzip2_base.riscv input.program 5 1> /dev/null
echo - 401.bzip2
cd /home/jerry/spec2006/Speckle/build/401.bzip2_test
time ./bzip2_base.riscv dryer.jpg 2 1> /dev/null
echo - 403.gcc
cd /home/jerry/spec2006/Speckle/build/403.gcc_test
time ./gcc_base.riscv cccp.i -o cccp.s 1> /dev/null
echo - 429.mcf
cd /home/jerry/spec2006/Speckle/build/429.mcf_test
time ./mcf_base.riscv inp.in 1> /dev/null
echo - 445.gobmk
cd /home/jerry/spec2006/Speckle/build/445.gobmk_test
time ./gobmk_base.riscv --quiet --mode gtp < capture.tst 1> /dev/null
echo - 445.gobmk
cd /home/jerry/spec2006/Speckle/build/445.gobmk_test
time ./gobmk_base.riscv --quiet --mode gtp < connect.tst 1> /dev/null
echo - 445.gobmk
cd /home/jerry/spec2006/Speckle/build/445.gobmk_test
time ./gobmk_base.riscv --quiet --mode gtp < connect_rot.tst 1> /dev/null
echo - 445.gobmk
cd /home/jerry/spec2006/Speckle/build/445.gobmk_test
time ./gobmk_base.riscv --quiet --mode gtp < connection.tst 1> /dev/null
echo - 445.gobmk
cd /home/jerry/spec2006/Speckle/build/445.gobmk_test
time ./gobmk_base.riscv --quiet --mode gtp < connection_rot.tst 1> /dev/null
echo - 445.gobmk
cd /home/jerry/spec2006/Speckle/build/445.gobmk_test
time ./gobmk_base.riscv --quiet --mode gtp < cutstone.tst 1> /dev/null
echo - 445.gobmk
cd /home/jerry/spec2006/Speckle/build/445.gobmk_test
time ./gobmk_base.riscv --quiet --mode gtp < dniwog.tst 1> /dev/null
echo - 456.hmmer
cd /home/jerry/spec2006/Speckle/build/456.hmmer_test
time ./hmmer_base.riscv --fixed 0 --mean 325 --num 45000 --sd 200 --seed 0 bombesin.hmm 1> /dev/null
echo - 458.sjeng
cd /home/jerry/spec2006/Speckle/build/458.sjeng_test
time ./sjeng_base.riscv test.txt 1> /dev/null
echo - 462.libquantum
cd /home/jerry/spec2006/Speckle/build/462.libquantum_test
time ./libquantum_base.riscv 33 5 1> /dev/null
echo - 464.h264ref
cd /home/jerry/spec2006/Speckle/build/464.h264ref_test
time ./h264ref_base.riscv -d foreman_test_encoder_baseline.cfg 1> /dev/null
echo - 471.omnetpp
cd /home/jerry/spec2006/Speckle/build/471.omnetpp_test
time ./omnetpp_base.riscv omnetpp.ini 1> /dev/null
echo - 473.astar
cd /home/jerry/spec2006/Speckle/build/473.astar_test
time ./astar_base.riscv lake.cfg 1> /dev/null
echo - 483.xalancbmk
cd /home/jerry/spec2006/Speckle/build/483.xalancbmk_test
time ./Xalan_base.riscv -v test.xml xalanc.xsl 1> /dev/null
