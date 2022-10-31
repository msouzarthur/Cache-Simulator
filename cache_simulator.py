# -*- coding: utf-8 -*-
"""
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

import os.path
import math
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
        
        #pos = posicao vazia ou -1
        pos = isLineFull(cacheIndex)
        
        #fHit = posicao de hit ou -1
        fHit = isHit(cacheIndex,intTag)
        
        #se gerou um hit
        if mem[cacheIndex][fHit][1]==intTag and fHit!=-1:
            nHits+=1    
            #tratativa de lru
            #atualiza o valor LRU
            if subs=='L':
                for j in range(nAssoc):
                    if mem[cacheIndex][fHit][2] > mem[cacheIndex][j][2]:
                        mem[cacheIndex][j][2] += 1
                mem[cacheIndex][fHit][2] = 0    
        #se validade é zero e gerou um miss       
        elif mem[cacheIndex][pos][0] == 0 and pos!=-1:
            #gera miss compulsorio
            mem[cacheIndex][pos][0] = 1
            mem[cacheIndex][pos][1] = intTag
            nMissComp += 1
            #tratativa de LRU
            if subs=='L':
                mem[cacheIndex][pos][2] = 0
                for j in range(nAssoc):
                    if j != pos and mem[cacheIndex][j][2]!=None:
                        mem[cacheIndex][j][2] += 1 
        #se linha cheia e miss
        elif pos == -1 and fHit==-1:
            #se cache está cheia
            if isFull():
                nMissCap+=1
            else:
                nMissConf+=1
            #tratativa de random
            if subs == 'R':
                rPos = 0 
                if nAssoc>1:
                    rPos = random.randint(0, nAssoc-1)
                mem[cacheIndex][rPos][1] = intTag
            #tratativa de fifo
            elif subs == 'F':
                fPos = fifoList[cacheIndex]
                mem[cacheIndex][fPos][1] = intTag
                if fPos == nAssoc-1:
                    fifoList[cacheIndex] = 0
                else:
                    fifoList[cacheIndex] = fPos+1
            #tratativa de LRU
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
                
        '''descomentar para debugging   
        printCache()
        print('{} {} {} '.format(cacheIndex, target, number))
        input("")'''
        line = f.read(4)
                 
def isHit(line, tag):
    #retorna posicao de hit ou -1
    global mem, nAssoc
    for p in range(nAssoc):
        if mem[line][p][1] == tag:
            return p
    return -1
    
def isLineFull(line):
    #retorna posicao livre ou -1 se estiver cheia
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
    print("i",end='\t')
    print("[val,tag]")
    for l in range(nSets):
        print(l,end="\t")
        print(mem[l])


def printEx():
    #exibe as informacoes finais
    global nAccess, nHits, nMiss, nMissComp, nMissCap, nMissConf, nFlag, nSets, subs
    nMiss = nMissComp + nMissCap + nMissConf
    if nFlag == 0:
        printCache()
        print('politica - {}'.format(subs))
        print('acessos - {}'.format(nAccess))
        print('hits - {:.2f}%'.format(100*(nHits/nAccess)))
        print('misses - {:.2f}%'.format(100*(nMiss/nAccess)))
        print('misses compulsorios - {:.2f}%'.format(100*(nMissComp/(nMiss))))
        print('misses capacidade - {:.2f}%'.format(100*(nMissCap/(nMiss))))
        print('misses conflito - {:.2f}%'.format(100*(nMissConf/(nMiss))))
    elif nFlag == 1:
        print('{}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}'.format(nAccess, nHits/nAccess, nMiss/nAccess, nMissComp/(nMiss), nMissCap/(nMiss), nMissConf/(nMiss)))        

        
def readCommand():
    #leitura de entrada
    global file, nAssoc, nBlockSize, nSets, nFlag, subs, mem
    cmd = input("> ")

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
    file = r"./"+file
    
    if not os.path.isfile(file):
        print("> arquivo {} não encontrado".format(file))
        readCommand()
        
if __name__=='__main__':
    main()
