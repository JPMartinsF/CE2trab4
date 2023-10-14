import numpy as np
import scipy as sp
from math import cos, exp, pi, radians

def tamanhoMatrizGn(*args):
    tamanho = 0
    for lista in args:
        for el in lista:
            if int(el["No1"]) > tamanho:
                tamanho = int(el["No1"])
            if int(el["No2"]) > tamanho:
                tamanho = int(el["No2"])
    return tamanho

def lerNetList(netlist):
    chavesResistores = ["Nome", "No1", "No2", "Valor"]
    chavesFonteCorrenteIndep = ["Nome", "No1", "No2", "Tipo", "Valor", "Amplitude", "Freq", "Fase"]
    chavesFonteTensaoIndep = ["Nome", "No1", "No2", "Tipo", "Valor", "Amplitude", "Freq", "Fase", "Variavel"]
    chavesFonteCorrenteContTensao = ["Nome", "No1", "No2", "Controle1", "Controle2", "Valor"]
    chavesFonteCorrenteContCorrente = ["Nome", "No1", "No2", "Controle1", "Controle2", "Valor", "Variavel"]
    chavesFonteTensaoContTensao = ["Nome", "No1", "No2", "Controle1", "Controle2", "Valor", "Variavel"]
    chavesFonteTensaoContCorrente = ["Nome", "No1", "No2", "Controle1", "Controle2", "Valor", "Variavel1", "Variavel2"]
    chavesCapacitor = ["Nome", "No1", "No2", "Valor", "CondicaoInicial"]
    chavesIndutor = ["Nome", "No1", "No2", "Valor", "CondicaoInicial", "Variavel"]
    chavesTransformador = ["Nome", "NoA", "NoB", "NoC", "NoD", "Valor1", "Valor2", "ValorMutuo", "Variavel1", "Variavel2"]
    chavesDiodo = ["Nome", "No1", "No2", "Is", "nVt"]
    with open(netlist, "r", encoding="utf-8") as arqNet:
        listaResistores = []
        listaFontesCorrenteIndep = []
        listaFontesTensaoIndep = []
        listaFontesCorrenteContTensao = []
        listaFontesCorrenteContCorrente = []
        listaFontesTensaoContTensao = []
        listaFontesTensaoContCorrente = []
        listaCapacitores = []
        listaIndutores =[]
        listaTransformadores = []
        listaDiodos = []
        numVariaveisExtras = 0
        for line in arqNet:
            if line != '\n' and line[0] != "*":
                #print(f"{line} é a linha atual")
                info = line.split()
                #print(info)
                if line[0] == "R":
                    dictInfo = dict(zip(chavesResistores, info))
                    listaResistores.append(dictInfo)
                elif line[0] == "I":
                    dictInfo = dict(zip(chavesFonteCorrenteIndep, info))
                    listaFontesCorrenteIndep.append(dictInfo)
                elif line[0] == "V":
                    numVariaveisExtras+=1
                    info += [numVariaveisExtras]
                    dictInfo = dict(zip(chavesFonteTensaoIndep, info))
                    listaFontesTensaoIndep.append(dictInfo)
                elif line[0] == "G":
                    dictInfo = dict(zip(chavesFonteCorrenteContTensao, info))
                    listaFontesCorrenteContTensao.append(dictInfo)
                elif line[0] == "F":
                    numVariaveisExtras+=1
                    info += [numVariaveisExtras]
                    dictInfo = dict(zip(chavesFonteCorrenteContCorrente, info))
                    listaFontesCorrenteContCorrente.append(dictInfo)
                elif line[0] == "E":
                    numVariaveisExtras+=1
                    info += [numVariaveisExtras]
                    dictInfo = dict(zip(chavesFonteTensaoContTensao, info))
                    listaFontesTensaoContTensao.append(dictInfo)
                elif line[0] == "H":
                    numVariaveisExtras+=1
                    info += [numVariaveisExtras]
                    numVariaveisExtras+=1
                    info += [numVariaveisExtras]
                    dictInfo = dict(zip(chavesFonteTensaoContCorrente, info))
                    listaFontesTensaoContCorrente.append(dictInfo)
                elif line[0] == "C":
                    dictInfo = dict(zip(chavesCapacitor, info))
                    listaCapacitores.append(dictInfo)
                elif line[0] == "L":
                    numVariaveisExtras+=1
                    info+= [numVariaveisExtras]
                    dictInfo = dict(zip(chavesIndutor, info))
                    listaIndutores.append(dictInfo)
#                elif line[0] == "K":
                    
                elif line[0] == "D":
                    dictInfo = dict(zip(chavesDiodo, info))
                    listaDiodos.append(dictInfo)

    return listaResistores, listaFontesCorrenteIndep, listaFontesTensaoIndep, \
        listaFontesCorrenteContTensao, listaFontesCorrenteContCorrente, listaFontesTensaoContTensao, \
            listaFontesTensaoContCorrente, numVariaveisExtras, listaCapacitores, listaIndutores, listaDiodos

def montaMatrizes(listaResistores, listaFontesCorrenteIndep, listaFontesTensaoIndep, \
    listaFontesCorrenteContTensao, listaFontesCorrenteContCorrente, listaFontesTensaoContTensao, \
        listaFontesTensaoContCorrente, numVariaveisExtras, listaCapacitores, listaIndutores, listaDiodos, passo):
    #MANTER PARA TER CONTROLE DO NÚMERO DAS VARIÁVEIS EXTRAS
    numNos = tamanhoMatrizGn(listaResistores, listaFontesCorrenteIndep, listaFontesCorrenteContTensao) 
    #print(numNos, numVariaveisExtras)
    matrizGn = np.zeros((numNos + numVariaveisExtras + 1, numNos + numVariaveisExtras + 1), dtype="complex_")
    listaI = np.zeros(numNos + numVariaveisExtras + 1, dtype="complex_")
    #FEITO
    for resistor in listaResistores:
        #print(resistor)
        matrizGn[int(resistor["No1"])][int(resistor["No1"])] += 1/float(resistor["Valor"])
        matrizGn[int(resistor["No1"])][int(resistor["No2"])] -= 1/float(resistor["Valor"])
        matrizGn[int(resistor["No2"])][int(resistor["No1"])] -= 1/float(resistor["Valor"])
        matrizGn[int(resistor["No2"])][int(resistor["No2"])] += 1/float(resistor["Valor"])
    #FEITO
    for fonteCorrContTens in listaFontesCorrenteContTensao:
        #print(fonteCorrContTens)
        matrizGn[int(fonteCorrContTens["No1"])][int(fonteCorrContTens["Controle1"])] += float(fonteCorrContTens["Valor"])
        matrizGn[int(fonteCorrContTens["No1"])][int(fonteCorrContTens["Controle2"])] -= float(fonteCorrContTens["Valor"])
        matrizGn[int(fonteCorrContTens["No2"])][int(fonteCorrContTens["Controle1"])] -= float(fonteCorrContTens["Valor"])
        matrizGn[int(fonteCorrContTens["No2"])][int(fonteCorrContTens["Controle2"])] += float(fonteCorrContTens["Valor"])
    #FEITO
    for fonteCorrContCorr in listaFontesCorrenteContCorrente:
        #print(fonteCorrContCorr)
        matrizGn[int(fonteCorrContCorr["No1"])][numNos + fonteCorrContCorr["Variavel"]] += float(fonteCorrContCorr["Valor"])
        matrizGn[int(fonteCorrContCorr["No2"])][numNos + fonteCorrContCorr["Variavel"]] -= float(fonteCorrContCorr["Valor"])
        matrizGn[int(fonteCorrContCorr["Controle1"])][numNos + fonteCorrContCorr["Variavel"]] += 1
        matrizGn[int(fonteCorrContCorr["Controle2"])][numNos + fonteCorrContCorr["Variavel"]] -= 1
        matrizGn[numNos + fonteCorrContCorr["Variavel"]][int(fonteCorrContCorr["Controle1"])] -= 1
        matrizGn[numNos + fonteCorrContCorr["Variavel"]][int(fonteCorrContCorr["Controle2"])] += 1
    #FEITO
    for fonteTensContTens in listaFontesTensaoContTensao:
        #print(fonteTensContTens)
        matrizGn[int(fonteTensContTens["No1"])][numNos + fonteTensContTens["Variavel"]] += 1
        matrizGn[int(fonteTensContTens["No2"])][numNos + fonteTensContTens["Variavel"]] -= 1
        matrizGn[numNos + fonteTensContTens["Variavel"]][int(fonteTensContTens["No1"])] -= 1
        matrizGn[numNos + fonteTensContTens["Variavel"]][int(fonteTensContTens["No2"])] += 1
        matrizGn[numNos + fonteTensContTens["Variavel"]][int(fonteTensContTens["Controle1"])] += float(fonteTensContTens["Valor"])
        matrizGn[numNos + fonteTensContTens["Variavel"]][int(fonteTensContTens["Controle2"])] -= float(fonteTensContTens["Valor"])
    #FEITO
    for fonteTensContCorr in listaFontesTensaoContCorrente:
        #print(fonteTensContCorr)
        matrizGn[int(fonteTensContCorr["No1"])][numNos + fonteTensContCorr["Variavel2"]] += 1
        matrizGn[int(fonteTensContCorr["No2"])][numNos + fonteTensContCorr["Variavel2"]] -= 1
        matrizGn[int(fonteTensContCorr["Controle1"])][numNos + fonteTensContCorr["Variavel1"]] += 1
        matrizGn[int(fonteTensContCorr["Controle2"])][numNos + fonteTensContCorr["Variavel1"]] -= 1
        matrizGn[numNos + fonteTensContCorr["Variavel1"]][int(fonteTensContCorr["Controle1"])] -= 1
        matrizGn[numNos + fonteTensContCorr["Variavel1"]][int(fonteTensContCorr["Controle2"])] += 1
        matrizGn[numNos + fonteTensContCorr["Variavel2"]][int(fonteTensContCorr["No1"])] -= 1
        matrizGn[numNos + fonteTensContCorr["Variavel2"]][int(fonteTensContCorr["No2"])] += 1
        matrizGn[numNos + fonteTensContCorr["Variavel2"]][numNos + fonteTensContCorr["Variavel1"]] += float(fonteTensContCorr["Valor"])
    #FEITO
    for fonteCorrIndep in listaFontesCorrenteIndep:
        #print(fonteCorrIndep)
        if fonteCorrIndep["Tipo"] == "DC":
            listaI[int(fonteCorrIndep["No1"])] -= float(fonteCorrIndep["Valor"])
            listaI[int(fonteCorrIndep["No2"])] += float(fonteCorrIndep["Valor"])
        else:
            listaI[int(fonteCorrIndep["No1"])] -= float(fonteCorrIndep["Valor"]) + float(fonteCorrIndep["Amplitude"]) * exp(radians(float(fonteCorrIndep["Fase"])))
            listaI[int(fonteCorrIndep["No2"])] += float(fonteCorrIndep["Valor"]) + float(fonteCorrIndep["Amplitude"]) * exp(radians(float(fonteCorrIndep["Fase"])))
    #FONTE DE TENSÃO INDEP OK!    
    for fonteTensIndep in listaFontesTensaoIndep:
        #print(fonteTensIndep)
        if fonteTensIndep["Tipo"] == "DC":
            listaI[numNos + fonteTensIndep["Variavel"]] -= float(fonteTensIndep["Valor"]) + float(fonteTensIndep["Amplitude"]) * exp(radians(float(fonteTensIndep["Fase"])))
            matrizGn[int(fonteTensIndep["No1"])][numNos + fonteTensIndep["Variavel"]] += 1
            matrizGn[int(fonteTensIndep["No2"])][numNos + fonteTensIndep["Variavel"]] -= 1
            matrizGn[numNos + fonteTensIndep["Variavel"]][int(fonteTensIndep["No1"])] -= 1
            matrizGn[numNos + fonteTensIndep["Variavel"]][int(fonteTensIndep["No2"])] += 1
        else:
            listaI[numNos + fonteTensIndep["Variavel"]] -= float(fonteTensIndep["Valor"])
            matrizGn[int(fonteTensIndep["No1"])][numNos + fonteTensIndep["Variavel"]] += 1
            matrizGn[int(fonteTensIndep["No2"])][numNos + fonteTensIndep["Variavel"]] -= 1
            matrizGn[numNos + fonteTensIndep["Variavel"]][int(fonteTensIndep["No1"])] -= 1
            matrizGn[numNos + fonteTensIndep["Variavel"]][int(fonteTensIndep["No2"])] += 1
    
    for capacitor in listaCapacitores:
        valor = int(capacitor["Valor"]/passo)
        matrizGn[int(int(capacitor["No1"]))][int(capacitor["No1"])] += valor
        matrizGn[int(int(capacitor["No1"]))][int(capacitor["No2"])] -= valor
        matrizGn[int(int(capacitor["No2"]))][int(capacitor["No2"])] -= valor
        matrizGn[int(int(capacitor["No2"]))][int(capacitor["No1"])] += valor
        listaI[int(capacitor["No1"])] += valor*int(capacitor["CondicaoInicial"])
        listaI[int(capacitor["No2"])] -= valor*int(capacitor["CondicaoInicial"])
    
    for indutor in listaIndutores:
        valor = int(indutor["Valor"])/passo
        matrizGn[int(indutor["No1"])][numNos + indutor["Variavel"]] += 1
        matrizGn[int(indutor["No2"])][numNos + indutor["Variavel"]] -= 1
        matrizGn[numNos + indutor["Variavel"]][int(indutor["No1"])] -= 1
        matrizGn[numNos + indutor["Variavel"]][int(indutor["No2"])] += 1
        matrizGn[numNos + indutor["Variavel"]][numNos + indutor["Variavel"]] += valor
        listaI[int(indutor["No1"])] += valor*int(indutor["CondicaoInicial"])

    for diodo in listaDiodos:
        G0 = int(diodo["Is"]) * (exp(0.45/int(diodo["nVt"])))/int(diodo["nVt"])
        I0 = int(diodo["Is"]) * (exp(0.45/int(diodo["nVt"]))-1) - G0*0.45
        listaI[diodo["No1"]] -= I0
        listaI[diodo["No2"]] += I0
        if G0 != 0:
            matrizGn[diodo["No1"]][diodo["No1"]] += 1/G0
            matrizGn[diodo["No1"]][diodo["No2"]] -= 1/G0
            matrizGn[diodo["No2"]][diodo["No1"]] -= 1/G0
            matrizGn[diodo["No2"]][diodo["No2"]] += 1/G0

    return matrizGn[1:,1:], listaI[1:]

def main(arqNetList, tSim, passo, tol, v0, vout):
    listaResistores, listaFontesCorrenteIndep, listaFontesTensaoIndep, \
        listaFontesCorrenteContTensao, listaFontesCorrenteContCorrente, listaFontesTensaoContTensao, \
            listaFontesTensaoContCorrente, numVariaveisExtras, listaCapacitores, listaIndutores, listaDiodos = lerNetList(arqNetList)
    qtdIteracao = int(tSim/passo + 1)
    matrizE = []
    print("qtdIt",qtdIteracao)
    matrizSaida = np.zeros([len(vout), qtdIteracao])
    for iteracao in range(qtdIteracao):
        matrizGn, listaI = montaMatrizes(listaResistores, listaFontesCorrenteIndep, listaFontesTensaoIndep, \
            listaFontesCorrenteContTensao, listaFontesCorrenteContCorrente, listaFontesTensaoContTensao, \
            listaFontesTensaoContCorrente, numVariaveisExtras, listaCapacitores, listaIndutores, listaDiodos, passo)
        print("Gn:",matrizGn)
        print("I:",listaI)
        matrizE = np.linalg.solve(matrizGn, listaI)
        print("E:",matrizE)
        for index in range(len(vout)):
            print("Index:",index)
            print("Saida:", matrizSaida)
            matrizSaida[index][iteracao] += matrizE[vout[index]-1]

    return matrizSaida

#Netlist1: OK
print(f"Netlist 1: \n{main('netlist1.txt', 1e-3, 0.2e-3, 1e-4, [1,0.5], [1,2])}")
#Netlist2: OK 
#print(f"Netlist 2: {main('netlist2.txt')}")
#Netlist3: OK 
#print(f"Netlist 3: {main('netlist3.txt')}")
#Netlist4: OK
#print(f"Netlist 4: {main('netlist4.txt')}")
