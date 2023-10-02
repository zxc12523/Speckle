import os
import glob
import csv
import pandas as pd

from decimal import *
getcontext().prec = 6

data = []
# fields = ('A','Float','RV32A','RV32C','RV32D','RV32F','RV32I','RV32M','RV64A','RV64I','RV64M','RV64V','Zicsr','nclas','sum')
fields = ('A', 'SVE', 'PCrel addr',  'Add/Sub (imm)', 'Logical (imm)', 'Move Wide (imm)', 'Bitfield', 
           'Extract', 'Cond Branch (imm)', 'Exception Gen', 'NOP', 'Hints', 'Barriers', 
           'System Insn',  'System Reg',  'Branch (reg)', 'Branch (imm)',  'Cmp & Branch', 'Tst & Branch',
           'AdvSimd ldstmult', 'AdvSimd ldst', 'ldst excl',  'Load Reg (lit)', 'ldst pair', 'ldst reg (imm)',
           'Data Proc Reg',  'Scalar FP', 'sum')

dir = "/home/jerry/spec2006/Speckle/"
BENCHMARKS=("bzip2", "gcc",  "mcf", "gobmk" , "hmmer" , "sjeng"  ,"libquantum", "h264ref", "omnetpp" ,"astar", "Xalan")
target = "arm"

def prune(string: str):
    i = 0
    j = len(string) - 1

    while ('a' > string[i] or string[i] > 'z') and ('A' > string[i] or string[i] > 'Z') and string[i] != ')':
        i += 1
    
    while ('a' > string[j] or string[j] > 'z') and ('A' > string[j] or string[j] > 'Z') and string[j] != ')':
        j -= 1

    # print(string[i:j+1])
    
    return string[i:j+1]


for benchmark in BENCHMARKS:
    for file in glob.iglob('result_' + target + '*/*.out', recursive=True):

        if file.find(benchmark) == -1:
            continue
        
        fp = open(dir + file, 'r')

        lines = fp.readlines()    
        lines.pop(0)

        m = dict()
        sum = 0

        for line in lines:
            if line[0:5] != 'Class':
                continue

            line = line.split('\t')
            num = line[1].split(' ')[0][1:]

            if '0' > num[0] or num[0] > '9':
                continue

            count = int(num)
            category = prune(line[0][6:])
            

            if category not in m.keys():
                m.setdefault(category, 0)
            
            m[category] += count
            sum += count
        
        for key in m.keys():
            m[key] = round(m[key] / sum, 3)
            
        
        m.setdefault("sum", sum)
        # print()
        m.setdefault("A", '_'.join(file.split('/')[0].split('_')[2:]))
        
        data.append(dict(sorted(m.items())))

    # print(data)

    # data.insert(0, data.pop())
    # data.insert(0, data.pop())

        # for i in range(1, len(data)):
        #     data[i]['sum'] = round(data[i]['sum'] / data[0]['sum'], 3)
    
        # data[0]['sum'] = 1

    with open(dir + "stat_" + target + "/" + benchmark + "_output.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        
        writer.writeheader()
        
        for row in data:
            writer.writerow(row)
    
    data.clear()

    dataframe = pd.read_csv(dir + "stat_" + target + "/" + benchmark + "_output.csv")
    dataframe.sort_values("A", axis=0, ascending=True, inplace=True, na_position='first')
    dataframe['sum'] /= dataframe['sum'][4]
    print(dataframe)
    dataframe.to_csv(dir + "stat_" + target + "/" + benchmark + "_output.csv")

df = pd.DataFrame()


for benchmark in BENCHMARKS:
    for file in glob.iglob('stat_' + target + '/*', recursive=True):
        if file.find(benchmark) == -1:
            continue
        
        cur = pd.read_csv(file)
        df = pd.concat([df, cur])

df.to_csv('output_' + target + '.csv')