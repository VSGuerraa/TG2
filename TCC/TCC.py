import json
import random
import networkx as nx
import matplotlib.pyplot as plt
from dataclasses import dataclass




def gerador_Dados(nro_Nodos,nro_Links,nro_Req):

    implementacoes = {}
    funcao = {}
    requisicoes = {}

    for i in range (0,4):
    
        randval= random.randint(2,10)
        BRAM=randval*64
        DSP=random.randint(0,4)
        Lat=random.randint(100,200)
        Thro=random.randint(10,100)

        implementacoes[i] = {
        "nome" : "I" + str(i),
        "CLBs" : randval,
        "BRAM" : BRAM,
        "DSPs" : DSP,
        "Lat" : Lat,
        "Throughput": Thro
        }
    for j in range (0,6):

        funcao[j] = {
            "nome": "F" + str(j),
            "implementacao": implementacoes[random.randint(0,i)]
            }

    for k in range (0,nro_Req):
        rand_fun=random.randint(0,5)
        rand_nodo_S=random.randint(0,nro_Nodos-1)
        rand_nodo_D=random.randint(0,nro_Nodos-1)
        while rand_nodo_S==rand_nodo_D:
            rand_nodo_D=random.randint(0,nro_Nodos)
        
        aux=funcao[rand_fun]["implementacao"]
    
        requisicoes[k] = {
            "Nodo_S": rand_nodo_S,
            "Nodo_D": rand_nodo_D,
            "max_Lat": aux["Lat"],
            "min_T": aux["Throughput"],
            "funcao": funcao[random.randint(0,5)],
            "valor": random.randint(10,500)
            }

    G = nx.gnm_random_graph(nro_Nodos, nro_Links)
    '''
    #visualiza grafico em tela

    #subax1 = plt.subplot(121)
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show() 

    '''
    lista=list(G.edges)
    topologia_rede=[]
    

    for a in range(0,nro_Nodos):
        fpga=[]
        lista_Links=[]
        lista_Part=[]
        for b in lista:
            nodoS = b[0]
            nodoD = b[1]
            if nodoD == a:
                lista_Links.append(nodoS)
            if nodoS == a:
                lista_Links.append(nodoD)
        for c in range(0,len(lista_Links)):
            thro=random.randint(100,1000)
            lat= random.randint(5,200)
            lista_Links[c]={lista_Links[c]: {"Lat": lat, "Throughput": thro}}
        
        lista_Part=[]
        nro_fpga=random.randint(0,3)
        if nro_fpga!=0:
            for i in range(nro_fpga):
                
                parts=random.randint(1,4)
                
                for j in range(0,parts):
                    clb=random.randint(5,50)
                    bram=random.randint(1,10)*128
                    dsp=random.randint(0,8)
                    lista_Part.append({"Part"+str(j): {"CLBs": clb, "BRAM":bram, "DSP": dsp }})
            fpga.append(lista_Part)
        
        topologia_rede.append({"Nodo"+str(a): {"FPGA": fpga, "Links": lista_Links}})
     
    with open ("requisicoes.json","w") as outfile:
        json.dump(requisicoes, outfile)

    with open ("funcoes.json","w") as outfile:
        json.dump(funcao, outfile)

    with open ("implementacoes.json","w") as outfile:
        json.dump(implementacoes, outfile)

    with open ("topologia.json","w") as outfile:
        json.dump(topologia_rede, outfile)


   # print("Arquivos Gerados")


def dfs_caminhos(grafo, inicio, fim):
    pilha = [(inicio, [inicio])]
    while pilha:
        vertice, caminho = pilha.pop()
        for proximo in set(grafo[vertice]) - set(caminho):
            if proximo == fim:
                yield caminho + [proximo]
            else:
                pilha.append((proximo, caminho + [proximo]))

@dataclass
class Function:
    name_func:str
    name_imp:str
    clb:int
    bram:int
    dsp:int

@dataclass
class Req:
    init_node:str
    out_node:str
    max_Lat:int
    min_T:int
    func:Function
    price:float

@dataclass
class Partition:
    clb:int
    bram:int
    dsp:int

@dataclass
class Link:
    nodo_d: str
    max_Lat: int
    min_T: int

@dataclass
class Node:
    fpga:int
    part: Partition
    link: Link


def ler_Dados():
    with open("requisicoes.json") as file1:
        requisicoes = json.load(file1)


    with open("topologia.json") as file2:
        topologia = json.load(file2)
    

    nodos=[]
    parts=[]
    links=[]
    lista_Caminhos=[]
    caminhos=[]
    lista_Parts=[]
    lista_Req=[]
    lista_Nodos=[]
   
    
    

    for i,v in enumerate(topologia):
        
        nodos.append(str(*v.keys()))
        parts=(v[nodos[i]]["FPGA"])
        links=(v[nodos[i]]["Links"])
        nro_FPGA=0
        caminhos=[]
        aux_Lista=[]
        lista_Links=[]

        for j in links:
            nodo_d=str(*j.keys())   
            lat=j[nodo_d]["Lat"]
            thro=j[nodo_d]["Throughput"]
            const_Link=Link(nodo_d,lat,thro)
            lista_Links.append(const_Link)
            caminhos.append(int(nodo_d))
        lista_Caminhos.append(caminhos)
    
        for a in parts: 
            for b in a:
                nodo=str(*b.keys())
                if nodo=='Part0':
                    nro_FPGA+=1
                clb=b[nodo]["CLBs"]
                bram=b[nodo]["BRAM"]
                dsp=b[nodo]["DSP"]
                const_Part=Partition(clb,bram,dsp)
                aux_Lista.append(const_Part)
            lista_Parts.append(aux_Lista)
        const_Nodo=Node(nro_FPGA,aux_Lista,lista_Links)
        
        lista_Nodos.append(const_Nodo)
                    
    for a,val in enumerate(requisicoes.values()):
        nodo_S=val["Nodo_S"]
        nodo_D=val["Nodo_D"]
        lat=val["max_Lat"]
        thro=val["min_T"]
        nome_F=val["funcao"]["nome"]
        imp=val["funcao"]["implementacao"]
        valor=val["valor"]
        nome_I=imp["nome"]
        clb=imp["CLBs"]
        bram=imp["BRAM"]
        dsp=imp["DSPs"]
        lat=imp["Lat"]
        thro=imp["Throughput"]
        c_Func=Function(nome_F,nome_I,clb,bram,dsp)
        c_Req=Req(nodo_S,nodo_D,lat,thro,c_Func,valor)
        lista_Req.append(c_Req)

    return lista_Req,lista_Caminhos,lista_Nodos



def check_Path(node_D,nodos,req):
    valid_Path=0
    new_Thro=None
    
    for nodo in nodos:
        if int(nodo.nodo_d)==node_D:
            if nodo.max_Lat<=req.max_Lat:
                if nodo.min_T>=req.min_T:
                    new_Thro=nodo.min_T-req.min_T
                    valid_Path=1
                    
    return [valid_Path,node_D,new_Thro]
#checa se o caminho do nodo inicial até o final é válido em relação a latência e vazão





def greedy(lista_Req,lista_Paths,lista_Nodos):
    aloc_Req=[]
    cash=0
    for req in lista_Req:
        path=list(dfs_caminhos(lista_Paths,req.init_node,req.out_node))
        path_Ord=sorted(path,key=len)
        check_Node=False
        check_Link=1
        refresh_Links=[]
        

        if lista_Nodos[req.init_node].fpga!=0:
            for a,parts in enumerate(lista_Nodos[req.init_node].part):
                if parts.clb>=req.func.clb:
                    if parts.bram>=req.func.bram:
                        if parts.dsp>=req.func.dsp:
                            check_Node=True
                            break

        for p in path_Ord:
            for b,c in zip(p,p[1:]):
                lista_Check=check_Path(c,lista_Nodos[b].link,req)
                check_Link+=lista_Check[0]
                aux_Lista=b,lista_Check[1],lista_Check[2]
                refresh_Links.append(aux_Lista)
            if check_Link==len(p):
                check_Link=True
                break
            else:
                check_Link=False
        
        if check_Link and check_Node:
            
            aloc_Req.append(req)
            lista_Nodos[req.init_node].part.pop(a)
            for nodo_I,nodo_F,thro in refresh_Links:
                for l in (lista_Nodos[nodo_I].link):
                    if int(l.nodo_d)==nodo_F:
                        l.min_T=thro
            cash+=req.price


    ratio=len(aloc_Req)/len(lista_Req)


        
    #print("Requisicoes alocadas:",aloc_Req)
    print("Nr requisicoes alocadas:",len(aloc_Req),"\nRatio:",round(ratio,2),"%")

    return(len(aloc_Req), aloc_Req)
    

    


                            

        





lista_Results={}
dataset_1=[]
dataset_2=[]
dataset_3=[]


modo=input("1- Testar unitario\n2- Teste em escala\n")
if modo == '1':
    nodos_G=int(input("Numero de nodos da rede:\n"))
    links_G=int(input("Numero de links da rede:\n"))
    req=int(input("Numero de requisicoes:\n"))
    gerador_Dados(nodos_G, links_G,req)
    lista_Req,lista_Paths,lista_Nodos=ler_Dados()
    greedy(lista_Req,lista_Paths,lista_Nodos)
else:
    nr_teste=int(input("Numero de testes:\n"))
    for index in range (nr_teste):
        size=random.randint(5,40)
        nodos_G=size
        links_G=int(size*1.2)
        req=random.randint(int(size*0.8),int(size*2))
        gerador_Dados(nodos_G, links_G,req)
        lista_Req,lista_Paths,lista_Nodos=ler_Dados()
        results=greedy(lista_Req,lista_Paths,lista_Nodos)
        lista_Results.update({
            "Teste"+str(index):{
            "Lista Requisicoes": len(lista_Req),
            "Requiscoes alocadas": results[0]},
            "Nodos": len(lista_Nodos),
            })
        dataset_1.append(len(lista_Req))
        dataset_2.append(results[0])
        dataset_3.append(len(lista_Nodos))

    with open ("Req Alocadas.json","w") as outfile:
        json.dump(lista_Results, outfile)

    
    test=zip(dataset_1,dataset_2,dataset_3)
    lista_test=list(sorted(test, key=lambda teste: teste[0]))
    dataset_1,dataset_2,dataset_3 = zip(*lista_test)

    fig = plt.figure() 
    ax = fig.add_subplot(111) 
    ax.plot(dataset_1, dataset_2,color='tab:green') 
    ax2 = ax.twinx() 
    ax2.plot(dataset_1, dataset_3, color = 'tab:red') 
    plt.title('Numero de funcoes alocadas', fontweight="bold") 
    ax.grid() 
    ax.set_xlabel("Numero de requisicoes") 
    ax.set_ylabel(r"Requisicoes alocadas",color='tab:red') 
    ax2.set_ylabel(r"Numero de nodos", color='tab:green') 
    ax2.set_ylim(0, 50) 
    ax.set_ylim(0, 100)     
    plt.show() 








