import json
import random


implementacoes = {}




for i in range (0,4):
    
    randval= random.randint(5,15)
    BRAM=randval*128
    DSP=random.randint(0,4)
    Lat=random.randint(1,250)
    Thro=random.randint(1000,100000)

    implementacoes[i] = {
    "nome" : "I" + str(i+1),
    "CLBs" : randval,
    "BRAM" : BRAM,
    "DSPs" : DSP,
    "Lat" : Lat,
    "Throughput": Thro
    }
    



with open ("implementacoes.json","w") as outfile:
    json.dump(implementacoes, outfile)





funcao = {}


for j in range (0,6):
    
    funcao[j] = {
        "nome": "F" + str(j+1),
        "implementacao": implementacoes[random.randint(1,i-1)]
        }


with open ("funcoes.json","w") as outfile:
    json.dump(funcao, outfile)

requisicoes = {"Size": 0}

for k in range (1,10):
    
    requisicoes[k] = {
        "Nodo_S": random.randint(0,10),
        "Nodo_D": random.randint(0,10),
        "max_Lat": random.randint(10,300),
        "min_T": random.randint(100,10000),
        "funcao": funcao[random.randint(1,j-1)],
        "valor": random.randint(10,500)
        }
requisicoes["Size"]=k

with open ("requisicoes.json","w") as outfile:
    json.dump(requisicoes, outfile)





topologia_rede = {
    "Nodo1": {"FPGA": 1, "Part": {"Part1": {"CLBs": 50, "BRAM":40000, "DSP": 3}},
              "Links":{"2":{"Lat": 20, "Throughput":50000} ,"4":{"Lat": 50, "Throughput": 15000}}},
    "Nodo2": {"FPGA": 1, "Part": {"Part1": {"CLBs": 40, "BRAM":30000, "DSP": 0},"Part2": {"CLBs": 15, "BRAM":60000, "DSP": 0}},
              "Links":{"1":{"Lat": 20, "Throughput":50000},"5":{"Lat": 30, "Throughput":2000},"6":{"Lat": 120, "Throughput":6000}}},
    "Nodo3": {"FPGA": 1, "Part": {"Part1": {"CLBs": 20, "BRAM":40000, "DSP": 1},"Part2": {"CLBs": 40, "BRAM":20000, "DSP": 1},"Part3": {"CLBs": 20, "BRAM":10000, "DSP": 2}},
              "Links":{"4":{"Lat": 150, "Throughput":10000},"5":{"Lat": 60, "Throughput":35000}}},
    "Nodo4": {"FPGA": 1, "Part": {"Part1": {"CLBs": 10, "BRAM":20000, "DSP": 8},"Part2": {"CLBs": 5, "BRAM":5000, "DSP": 0}},
              "Links":{"1":{"Lat": 50, "Throughput":15000},"3":{"Lat": 150, "Throughput":10000},"7":{"Lat": 25, "Throughput":7000}}},
    "Nodo5": {"FPGA": 1, "Part": {"Part1": {"CLBs": 30, "BRAM":35000, "DSP": 5},"Part2": {"CLBs": 30, "BRAM":50000, "DSP": 3}},
              "Links":{"2":{"Lat": 30, "Throughput":2000},"3":{"Lat": 60, "Throughput":35000},"6":{"Lat": 70, "Throughput":25000}}},
    "Nodo6": {"FPGA": 1, "Part": {"Part1": {"CLBs": 40, "BRAM":100000, "DSP": 6}},
              "Links":{"2":{"Lat": 120, "Throughput":6000},"5":{"Lat": 70, "Throughput":25000},"7":{"Lat": 100, "Throughput":30000}}},
    "Nodo7": {"FPGA": 1, "Part": {"Part1": {"CLBs": 20, "BRAM":25000, "DSP": 4}, "Part2":{"CLBs": 10, "BRAM":10000, "DSP": 2},"Part3":{"CLBs": 10, "BRAM":10000, "DSP": 2}},
              "Links":{"4":{"Lat": 25, "Throughput":7000},"6":{"Lat": 100, "Throughput":30000}}}
        }



with open ("topologia.json","w") as outfile:
    json.dump(topologia_rede, outfile)


print("Arquivos Gerados")