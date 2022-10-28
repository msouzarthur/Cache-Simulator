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
from numpy import random

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
fifoCount = 0

def main():
    read() 
    build()
    run()
    printCache()

def read():
    #leitura de entrada
    global nSets, bSize, assoc, subs, flag, file
    
    #print("> cache_simulator <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada")
    cmd = input("> ")
    cmd = 'cache_simulator 256 1 2 R 1 bin_10000.bin'
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
    global bOffset, nSets, bSize, assoc, memSize, mem, subs
    
    for i in range(assoc):
        sets = []
        for k in range(int(nSets)):
            val = 0
            tag = None
            pol = None
            sets.append([val, tag, pol]) if subs=='L' else sets.append([val, tag])
        mem.append(sets)
    
    
def printCache():
    global nAcess, nHits, nMissComp, nMissCap, nMissConf
    nMiss = nMissComp+nMissCap+nMissConf
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
        print('{}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}'.format(nAcess, nHits/nAcess, nMiss/nAcess, nMissComp/(nMiss), nMissCap/(nMiss), nMissConf/(nMiss)))        
     
    
def run():
    global mem, nAcess, nHits, nMissComp, nMissCap, nMissConf, fifoCount
    
    f =  open(file,'rb')
    line = f.read(4)
    

    while line:
        fHit = False
        nAcess += 1
        number = int.from_bytes(line, byteorder='big', signed=False)

        target ='{:032b}'.format(number)
        #print(target)
        
        index = int(math.log(nSets,2))
        offset = int(math.log(bSize,2))
        tag = int(32-index-offset)
        
        #print("{} - {} - {} - {}".format(target,offset,index,tag))
        
        intOffset = int("".join(list(target[(32-offset):32])),2) if offset>0 else 0
        # ver erro
        intIndex = int("".join(list(target[(32-offset-index):32-offset])),2) if index>0 else 0
        
        intTag = int("".join(list(target[:(32-offset-index)])),2)
    
        cacheIndex = intIndex%nSets if intIndex > 0 else 0
        
        if assoc > 1:
            #Xndex = isLineFull(cacheIndex)
            #print(Xndex ,mem[0][cacheIndex][0],mem[1][cacheIndex][0],mem[2][cacheIndex][0],mem[3][cacheIndex][0])
            for p in range(assoc):
                if mem[p][cacheIndex][1] == intTag:
                    nHits+=1
                    fHit = True
                    if subs=='L':
                        for pp in range(assoc):
                            if mem[pp][cacheIndex][2] != None:
                                if mem[pp][cacheIndex][2] < mem[p][cacheIndex][2]:
                                    mem[pp][cacheIndex][2]+=1
                            mem[p][cacheIndex][2]=0
            if not fHit:
                setIndex = isLineFull(cacheIndex)
                if setIndex == -1 :
                    if isFull():
                        nMissCap+=1
                    else:
                        nMissConf+=1
                    if subs=='R':
                        randomSet = random.randint(0, assoc-1)
                        mem[randomSet][cacheIndex][1] = intTag
                    elif subs=='F':
                        
                        mem[fifoCount][cacheIndex][1] = intTag
                        if fifoCount < assoc - 1 :
                            fifoCount+=1 
                        else: 
                            fifoCount = 0
                    else: 
                        pos = findBiggerPol(cacheIndex)
                        for p in range(assoc):
                            mem[p][cacheIndex][2]+=1
                        mem[pos][cacheIndex][2] = 0
                else:
                    nMissComp+=1
                    mem[setIndex][cacheIndex][0] = 1
                    mem[setIndex][cacheIndex][1] = intTag             
                    if subs=='L':
                        mem[setIndex][cacheIndex][2] = 0
                        for p in range(assoc):
                            if setIndex != p and mem[p][cacheIndex][2]!=None:
                                mem[p][cacheIndex][2]+=1             
        else:
            if mem[0][cacheIndex][0] == 0:
                nMissComp+=1
                mem[0][cacheIndex][0] = 1
                mem[0][cacheIndex][1] = intTag
            elif mem[0][cacheIndex][1] == intTag:
                nHits+=1
            else:
                if isFull():
                    nMissCap+=1
                else:
                    nMissConf+=1
                mem[0][cacheIndex][1] = intTag 
        line = f.read(4)

def findBiggerPol(line):
    global mem, assoc
    for p in range(assoc):
        if mem[p][line][2] == assoc-1:
            return p
    return -1
                    

def isLineFull(line):
    global mem, assoc
    for p in range(assoc):
        if mem[p][line][0] == 0:
            return p
    return -1
        
        
            
def isFull():
    global mem
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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    