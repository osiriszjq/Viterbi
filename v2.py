 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov  6 15:16:56 2018

@author: jianqiaozheng
"""

import numpy as np


def sum1(x):
    return (int(x/8)+int((x%4)/2)+x%2)%2


def sum2(x):
    return (int(x/8)+int((x%8)/4)+int((x%4)/2)+x%2)%2


ifreach = np.zeros((8,8))
output = np.zeros((8,8))

for i in range(8):
    for j in range(8):
        if int(i/2)==j%4:
            ifreach[i][j] = 1
            x = int(j/4)*8+i
            o1 = sum1(x)
            o2 = sum2(x)
            output[i][j] = o1*2+o2

inbits = np.random.randint(0,2,128)
inbits[125] = 0
inbits[126] = 0
inbits[127] = 0

inseq = np.zeros(256)


current = 0
for i in range(128):
    current = inbits[i]*8+int(current/2)
    inseq[2*i] = sum1(current)
    inseq[2*i+1] = sum2(current)
  
path = []
for i in range(8):
    path.append([])
    
path_cost = np.zeros(8)

for i in range(8):
    if ifreach[0][i]==1:
        path_cost[i] = (inseq[0]!=int(output[0][i]/2))+(inseq[1]!=(output[0][i]%2))
        path[i].append(str(int(i/4)))
    else:
        path_cost[i] = np.inf
        path[i].append(str(9))
        

for k in range(1,128):
    print(k)
    tmp_path = []
    tmp_all_cost = np.inf*np.ones(8)
    for i in range(8):
        tmp_path.append([])
    for j in range(8):
        tmp_cost = np.inf
        tmp_i = 7
        for i in range(8):
            if path_cost[i] < np.inf:
                if ifreach[i][j]==1:
                    if tmp_cost == np.inf:
                        tmp_cost = path_cost[i]+(inseq[2*k]!=int(output[i][j]/2))+(inseq[2*k+1]!=(output[i][j]%2))
                        tmp_i = i
                    else:
                        if tmp_cost>path_cost[i]+(inseq[2*k]!=int(output[i][j]/2))+(inseq[2*k+1]!=(output[i][j]%2)):
                            tmp_cost = path_cost[i]+(inseq[2*k]!=int(output[i][j]/2))+(inseq[2*k+1]!=(output[i][j]%2))
                            tmp_i = i
                                
                        elif tmp_cost == path_cost[i]+(inseq[2*k]!=int(output[i][j]/2))+(inseq[2*k+1]!=(output[i][j]%2)):
                            tmp_i = [i,tmp_i]
        tmp_all_cost[j] = tmp_cost                    
        if isinstance(tmp_i,(list,)):
            if len(tmp_i) == 2:
                if isinstance(path[tmp_i[0]][0],(list,)):
                    tmp_path[j] = path[tmp_i[0]].copy()
                    if isinstance(path[tmp_i[1]][0],(list,)):
                        for l in range(len(path[tmp_i[1]])):
                            tmp_path[j].append(path[tmp_i[1]][l])
                    else:
                        tmp_path[j].append(path[tmp_i[1]])
                else :
                    if isinstance(path[tmp_i[1]][0],(list,)):
                        tmp_path[j] = path[tmp_i[1]].copy()
                        tmp_path[j].append(path[tmp_i[0]])
                    else:
                        tmp_path[j] = [path[tmp_i[0]][0],path[tmp_i[1]][0]]
                for l in range(len(tmp_path[j])):
                    tmp_path[j][l]+=str(int(j/4))
        else:
            tmp_path[j] = path[tmp_i].copy()
            if isinstance(tmp_path[j][0],(list,)):
                for l in range(len(tmp_path[j])):
                    tmp_path[j][l]+=str(int(j/4))
            else :
                tmp_path[j][0]+=str(int(j/4))                            
    path = tmp_path.copy()
    path_cost = np.copy(tmp_all_cost)

cost_last = path_cost[0]
path_last = path[0]
    
    