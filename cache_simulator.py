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
cache_simulator 128 2 4 R 1 bin_1000.bin
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

def main():
    readCommand()
    buildCache()
    printCache()
    runFile()
    #printEx()
    
def buildCache():
    global nAssoc, nSets, mem, subs
    #parametriza a cache
    
    #define o tipo de bloco
    if subs!='L':
        #validade, tag
        block = [0, None]
    else:
        #validade, tag, lru
        block = [0, None, None]
    
    for c in range(nSets):
        #percorre os indices
        sets = []
        #pra cada indice possui um bloco com assoc
        for i in range(nAssoc):
            sets.append(block)
        mem.append(sets)
    return False
    

def runFile():
    #testa o arquivo
    return False

def printCache():
    global mem, nSets
    for l in range(nSets):
        print(mem[l])


def printEx():
    #exibe as informacoes finais
    global nAccess, nHits, nMiss, nMissComp, nMissCap, nMissConf, nFlag
    
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
    bSize = int(cmd[2].strip())
    
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
