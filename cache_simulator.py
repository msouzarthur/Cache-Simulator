# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 07:46:43 2022

@author: arthur souza
@author: rafael grimmler
"""

'''
cache_simulator <nsets> <bsize> <assoc> <substituição> <flag_saida> arquivo_de_entrada
cache_simulator 256 4 1 R 1 bin_100.bin

cache_simulator 128 2 4 R 1 bin_1000.bin

cache_simulator 256 1 2 R 1 bin_10000.bin
cache_simulator 512 8 2 R 1 vortex.in.sem.persons.bin
'''

import pandas as pd
import os.path
import math
from pprint import pprint
from pprint import pp
from numpy import random

''' variáveis globais '''
#informacoes da cache
file = ''
nAssoc = 0
nBlockSize = 0 
nSets = 0
nFlag = 0
subs = 'R'
mem = []
#informacoes do teste
nAccess = 0
nHits = 0
nMiss = 0
nMissComp = 0
nMissCap = 0
nMissConf = 0
fifoList = []

def main():
    readCommand()
    buildCache()
    runFile()
    
    printEx()
    
def buildCache():
    global nAssoc, nSets, mem, subs, fifoList
    #parametriza a cache
    
    
    for c in range(nSets):
        #percorre os indices
        sets = []
        #pra cada indice possui um bloco com assoc
        for i in range(nAssoc):        
            #define o tipo de bloco
            if subs!='L':
                #validade, tag
                block = [0, None]
            else:
                #validade, tag, lru
                block = [0, None, None]
            sets.append(block)
        fifoList.append(0)
        mem.append(sets)
    return False
    

def runFile():
    #testa o arquivo
    global fifoList, mem, nAccess, nHits, nMiss, nMissComp, nMissCap, nMissConf, nBlockSize

    # le o arquivo
    f =  open(file,'rb')
    line = f.read(4)
    while line:
        fHit = False
        nAccess += 1
        number = int.from_bytes(line, byteorder='big', signed=False)
        #pega o endereco
        target ='{:032b}'.format(number)
       
        #calcula os bits das infos
        index = int(math.log(nSets,2))
        offset = int(math.log(nBlockSize,2))
        tag = int(32-index-offset)
        
        #calcula as infos em decimal
        intOffset = int("".join(list(target[(32-offset):32])),2) if offset>0 else 0
        intIndex = int("".join(list(target[(32-offset-index):32-offset])),2) if index>0 else 0
        intTag = int("".join(list(target[:(32-offset-index)])),2)
        
        #seleciona o index da memoria
        cacheIndex = intIndex%nSets if intIndex > 0 else 0
        
    
        #tá disponivel
        #print('tá full: ',isLineFull(cacheIndex))
        pos = isLineFull(cacheIndex)
        fHit = isHit(cacheIndex,intTag)
        #print('fhit: ',fHit)
        if mem[cacheIndex][fHit][1]==intTag and fHit!=-1:
            nHits+=1
            #print('deu hit')
            
            if subs=='L':
                for j in range(nAssoc):
                    if mem[cacheIndex][fHit][2] > mem[cacheIndex][j][2]:
                        mem[cacheIndex][j][2] += 1
                mem[cacheIndex][fHit][2] = 0
                
        elif mem[cacheIndex][pos][0] == 0 and pos!=-1:
            mem[cacheIndex][pos][0] = 1
            mem[cacheIndex][pos][1] = intTag
            nMissComp += 1
            
            if subs=='L':
                mem[cacheIndex][pos][2] = 0
                for j in range(nAssoc):
                    if j != pos and mem[cacheIndex][j][2]!=None:
                        mem[cacheIndex][j][2] += 1
                
        elif pos == -1 and fHit==-1:
            if isFull():
                nMissCap+=1
            else:
                nMissConf+=1
            if subs == 'R':
                rPos = random.randint(0, nAssoc-1)
                mem[cacheIndex][rPos][1] = intTag
            elif subs == 'F':
                fPos = fifoList[cacheIndex]
                mem[cacheIndex][fPos][1] = intTag
                if fPos == nAssoc-1:
                    fifoList[cacheIndex] = 0
                else:
                    fifoList[cacheIndex] = fPos+1
            elif subs == "L":
                lPos = 0
                for j in range(nAssoc):
                    mem[cacheIndex][j][2] += 1
                for j in range(nAssoc):
                    if mem[cacheIndex][j][2] == nAssoc:
                        lPos = j 
                        break
                mem[cacheIndex][lPos][2] = 0
                mem[cacheIndex][lPos][1] = intTag
                
                #se for miss conf
                #substitui o pol == nAssoc-1 e todos incrementam
            
        #printCache()
        #print('{} {} {} '.format(cacheIndex, target, number))
        #input("")
        line = f.read(4)

def findBiggerPol(line):
    global mem, nAssoc
    
    for p in range(nAssoc):
        if mem[line][p][2] == nAssoc-1:
            return p
    return -1
                    
def isHit(line, tag):
    global mem, nAssoc
    for p in range(nAssoc):
        if mem[line][p][1] == tag:
            return p
    return -1
    

def isLineFull(line):
    #retorna se a linha tá cheia
    global mem, nAssoc
    for p in range(nAssoc):
        if mem[line][p][0] == 0:
            return p
    return -1
        
        
            
def isFull():
    #retorna se a cache tá cheia
    global mem, nSets, nAssoc
    for r in range(nSets):
        for p in range(nAssoc):
            if mem[r][p][0] == 0:
                return False
    return True
    
def printCache():
    global mem, nSets
    for l in range(nSets):
        print(mem[l])


def printEx():
    #exibe as informacoes finais
    global nAccess, nHits, nMiss, nMissComp, nMissCap, nMissConf, nFlag
    nMiss = nMissComp + nMissCap + nMissConf
    if nFlag == 0:
        print('pandas')
    elif nFlag == 1:
        print('{}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}'.format(nAccess, nHits/nAccess, nMiss/nAccess, nMissComp/(nMiss), nMissCap/(nMiss), nMissConf/(nMiss)))        

        
def readCommand():
    #leitura de entrada
    global file, nAssoc, nBlockSize, nSets, nFlag, subs, mem
    cmd = input("> ")
    
    #cmd = 'cache_simulator 256 1 2 R 1 bin_10000.bin'
    
    #trata a falta da chamada para ter um padrao de comprimento
    if "cache_simulator" not in cmd:
        cmd += "cs "
    
    if len(cmd)<20:
        readCommand()
        
    cmd = cmd.split(" ")
    
    #define o numero de índices
    nSets = int(cmd[1].strip())
    
    #define o tamanho do bloco
    nBlockSize = int(cmd[2].strip())
    
    #define a associatividade
    nAssoc = int(cmd[3].strip())
    
    #define a politica de substituicao
    subs = cmd[4].strip()
    
    #define a flag de saida
    nFlag = int(cmd[5].strip())
    
    #trata o nome do arquivo
    file = cmd[6].strip()
    file = "./"+file
    
    if not os.path.isfile(file):
        print("> arquivo {} não encontrado".format(file))
        readCommand()
        
if __name__=='__main__':
    main()
