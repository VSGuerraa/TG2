import json
from dataclasses import dataclass
from os import strerror




class Function:
    name_func:str
    name_imp:str
    clb:int
    dsp:int
    bram:int
    lat:int
    thr:int


class Req:
    init_node:str
    out_node=str
    max_lat=int
    min_t=int
    func= Function
    price=float


class Partition:
    size:int
    clb:int
    dsp:int
    bram:int

class Link:
    nodo_d:str
    max_lat: int
    min_t:int
    

class Node:
    fpga:int
    part: Partition
    link: Link



with open("requisicoes.json") as file1:
    requisicoes = json.load(file1)


with open("topologia.json") as file2:
    topologia = json.load(file2)



for i in range (0,7):
    aux_str = list(topologia.values())
    Node[i].fpga = aux_str["FPGA"]
    
