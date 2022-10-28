# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 21:25:24 2022

@author: arthur souza
@author: rafael grimmler
"""

import pandas as pd
import os.path
import math
from pprint import pprint
from pprint import pp

assoc = 0
bSize = 0
bOffset = 0
flag = 0
file = '' 
nSets = 0
nAcess = 0
nHits = 0
nMissComp = 0
nMissCap = 0
nMissConf = 0
subs = 'R'
memSize = 0
mem = []

def main():
    read() 
    mem = build()
    printCache(mem)
    run(mem)

def read():
    #leitura de entrada
    global nSets, bSize, assoc, subs, flag, file
    
    #print("> cache_simulator <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada")
    cmd = input("> ")
    cmd = 'cache_simulator 8 1 1 R 1 bin_100.bin'
    if "cache_simulator" not in cmd:
        cmd += "c "
    cmd = cmd.split(" ")
    
    #define o numero de índices
    nSets = int(cmd[1].strip())
    
    #define o tamanho do bloco
    bSize = int(cmd[2].strip())
    
    #define a associatividade
    assoc = int(cmd[3].strip())
    
    #define a politica de substituicao
    subs = cmd[4].strip()
    
    #define a flag de saida
    flag = int(cmd[5].strip())
    
    #trata o nome do arquivo
    file = cmd[6].strip()
    file = "./"+file
    
    if not os.path.isfile(file):
        print("> arquivo {} não encontrado".format(file))
        read()
    

def build():
    #cria a memoria
    global bOffset, nSets, bSize, assoc, memSize
    
    mem = []
    
    for i in range(assoc):
        sets = []
        for k in range(int(nSets)):
            val = 0
            tag = None
            sets.append([val, tag])
        mem.append(sets)
    return mem
    
    
def printCache(mem):
    #exibe a memoria
    if flag == 0 :
        columns = ['validade','tag']
        df = pd.DataFrame(mem, columns = columns)
        print(df)
        print(df.describe())
        '''
        for sets in mem:
            print("[")
            for s in sets:
                print(end="\t")
                print(s)
            print("]")
        '''
    elif flag == 1:
        print('normal')        
        '''
            • flag_saida = 1
            o Formato padrão de saída que deverá respeitar a seguinte ordem: 
            Total de acessos, Taxa de hit, Taxa de miss, Taxa de miss compulsório, 
            Taxa de miss de capacidade, Taxa de miss de conflito 
            o Ex: 100000, 0.95, 0.06, 0.01, 0.02, 0.03
        '''        
    
def run(mem):
    f =  open(file,'rb')
    line = f.read(4)
    
    nAcess=0
    nHit = 0
    
    nCompul = 0
    nCap = 0
    nConf = 0
    
    while line:
        nAcess += 1
        number = int.from_bytes(line, byteorder='big', signed=False)

        target ='{:032b}'.format(number)
        #print(target)
        
        index = int(math.log(nSets,2))
        offset = int(math.log(bSize,2))
        tag = int(32-index-offset)
        
        #print("{} - {} - {} - {}".format(target,offset,index,tag))
        
        intOffset = int("".join(list(target[(32-offset):32])),2) if offset>0 else 0
        intIndex = int("".join(list(target[(32-offset-index):32-offset])),2)
        intTag = int("".join(list(target[:(32-offset-index)])),2)
    
        cacheIndex = intIndex%nSets if intIndex > 0 else 0
        
        if assoc > 1:
            for p in range(assoc):    
                mem[p][cacheIndex]
        else:
            if mem[0][cacheIndex][0] == 0:
                nCompul+=1
                mem[0][cacheIndex][0] = 1
                mem[0][cacheIndex][1] = intTag
            elif mem[0][cacheIndex][1] == intTag:
                nHit+=1
            else:
                if isFull(mem):
                    nCap+=1
                else:
                    nConf+=1

                mem[0][cacheIndex][1] = intTag
            
                
        print('cache index - {}'.format(cacheIndex))
        line = f.read(4)
           
    print(mem[0])
            
def isFull(mem):
    for r in range(nSets):
        for p in range(assoc):
            if mem[p][r][0] == 0:
                return False
    return True
            
    
        
    
if __name__ == "__main__":
    main()
    
    
    '''
    valor 20 tem indice 5 e offset 0 e tag 0
    tag pode ser 0 mesmo
    
    '''
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    