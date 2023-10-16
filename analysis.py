import subprocess
import json


def analysis(target, spec, opt):
    with open("/home/jerry/Speckle/result/{}+128_{}_{}/{}_base.{}.out".format(target, spec, opt, name, target), 'r') as fp,  \
        open('/home/jerry/Speckle/result/{}+128_{}_{}/{}.objdump.log'.format(target, spec, opt, target), 'a') as objfile,  \
        open('/home/jerry/Speckle/result/{}+128_{}_{}/{}.addr2line.log'.format(target, spec, opt, target), 'a') as addrfile,  \
        open('/home/jerry/Speckle/result/{}+128_{}_{}/{}.disassem.log'.format(target, spec, opt, target), 'a')as disfile:

        addrfile.truncate(0)
        objfile.truncate(0)
        disfile.truncate(0)

        subprocess.call(['/home/jerry/llvm-project/{}/bin/llvm-objdump'.format(target), '-d',
                        "/home/jerry/Speckle/result/{}+128_{}_{}/{}_base.{}".format(target, spec, opt, name, target)], 
                        stdout=objfile, 
                        shell=False)

        lines = fp.readlines()
        for line in lines:
            line = line.split(', ')
            pc = line[0]
            insns = line[2]
            count = line[3]

            subprocess.call(['/home/jerry/llvm-project/arm/bin/llvm-addr2line', '-Cfi', '-e', 
                            "/home/jerry/Speckle/result/{}+128_{}_{}/{}_base.{}".format(target, spec, opt, name, target), pc], 
                            stdout=addrfile, 
                            shell=False)

            
            subprocess.call(['grep', str(hex(int(pc[2:], 16)))[2:] + ':', 
                            '/home/jerry/Speckle/result/{}+128_{}_{}/{}.objdump.log'.format(target, spec, opt, target), 
                            '-A{}'.format(int(insns) - 1)], 
                            stdout=disfile, 
                            shell=False)
            
    with open("/home/jerry/Speckle/result/{}+128_{}_{}/{}_base.{}.out".format(target, spec, opt, name, target), 'r') as fp, \
        open('/home/jerry/Speckle/result/{}+128_{}_{}/{}.addr2line.log'.format(target, spec, opt, target), 'r') as addrfile,  \
        open('/home/jerry/Speckle/result/{}+128_{}_{}/{}.disassem.log'.format(target, spec, opt, target), 'r')as disfile, \
        open('/home/jerry/Speckle/result/{}+128_{}_{}/{}.log'.format(target, spec, opt, target), 'a') as logfile, \
        open('/home/jerry/Speckle/result/{}+128_{}_{}/{}.json'.format(target, spec, opt, target), 'a') as jsonfile:

        infolines = fp.readlines()
        addrlines = addrfile.readlines()
        dislines = disfile.readlines()

        logfile.truncate(0)
        jsonfile.truncate(0)

        i, j = 0, 0
        sum = 0

        d = {}
        
        for line in infolines:
            line = line.split(', ')
            pc = line[0]
            insns = line[2]
            count = line[3]

            logfile.write(', '.join(line))
            logfile.write(''.join(addrlines[i:i+2]))
            logfile.write(''.join(dislines[j:j+int(insns)]))

            if addrlines[i][:-1] not in d.keys():
                d.setdefault(addrlines[i][:-1], int(insns) * int(count))
            else:
                d[addrlines[i][:-1]] += int(insns) * int(count)

            i += 2
            j += int(insns)
            sum += int(insns) * int(count)

            # print(sum)

            # print(pc, int(insns)*int(count))
        
        d = dict(sorted(d.items()))
        json.dump([d, {'sum': sum}], jsonfile, sort_keys=True, indent=4)

target = 'riscv'
opts = ['O3', 'O3_Nloop', 'O3_Nslp', 'O3_Nslp_Nloop']
spec = '433.milc'
name = 'milc'

print('target: ', target)

for opt in opts:
    analysis(target, spec, opt)