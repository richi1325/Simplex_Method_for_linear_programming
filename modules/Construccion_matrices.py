import re
import numpy as np

def funcionObjetivo():
    while(True):
        tipo_simplex = input('¿El problema es de MAXIMIZAR (1) o MINIMIZAR (2)?:')
        if tipo_simplex in ['1','2']:
            tipo_simplex = int(tipo_simplex)
            break
        else:
            print('¡Inserta una opción válida!')
        
    z = input('Inserta la función objetivo:')
    z = re.sub(r'\s+','',z)
    variablesB = re.findall(r'[0-9]*\.*[0-9]*([a-zA-Z]+[0-9]*)',z)
    cB =  re.findall(r'(-*[0-9]*\.*[0-9]*)[a-zA-Z]+[0-9]*',z)
    for i in range(len(cB)):
        if cB[i]=='-':
            cB[i]=(-1)*tipo_simplex*-1.0
        elif cB[i]!='':
            cB[i]=(-1)*tipo_simplex*float(cB[i])
        else:
            cB[i]=(-1)*tipo_simplex*1.0
    return np.array(variablesB), np.array(cB)


def construirB(numero_restricciones_estandar,B_aux):
    B = list()
    for i in range(numero_restricciones_estandar):
        B.append([0.0 for _ in range(len(variablesB))])    

    for i in range(numero_restricciones_estandar):
        if len(B_aux[i])==len(variablesB) and re.findall(r'-*[0-9]*\.*[0-9]*([a-zA-Z]+[0-9]*)',restricciones[i]) == variablesB:
            for j in range(len(variablesB)):
                if re.search(r'-+[a-zA-Z]+',B_aux[i][j]):
                    B[i][j]=-1.0
                elif re.search(r'^-*[0-9]+',B_aux[i][j]):
                    x=re.search(r'^-*[0-9]+',B_aux[i][j])
                    B[i][j]=float(B_aux[i][j][x.start():x.end()])
                else:
                    B[i][j]=1.0
        else:
            posicion_variables=0
            posicion_B=0
            for j in range(len(variablesB)):
                if posicion_B>=len(B[i])-1:
                    posicion_B-=1
                x=re.search(r'[a-zA-Z]+[0-9]*$',B_aux[i][posicion_B])
                if variablesB[posicion_variables]!=B_aux[i][posicion_B][x.start():x.end()]:
                    B[i][j]=0.0
                    posicion_variables+=1
                else:
                    if re.search(r'-+[a-zA-Z]+',B_aux[i][posicion_B]):
                        B[i][j]=-1.0
                    elif re.search(r'^-*[0-9]+',B_aux[i][posicion_B]):
                        x=re.search(r'^-*[0-9]+',B_aux[i][posicion_B])
                        B[i][j]=float(B_aux[i][posicion_B][x.start():x.end()])
                    else:
                        B[i][j]=1.0
                    posicion_variables+=1
                    posicion_B+=1
    return B


def pseudoInvB(signoVariableNB):
    B_Pseudo_Inv=list()
    posicion=0
    for i in range(len(signoVariableNB)):
        aux=list()
        for j in range(len(signoVariableNB)):
            if posicion==j:
                aux.append(signoVariableNB[i])
            else:
                aux.append(0.0)
        posicion+=1
        B_Pseudo_Inv.append(aux)
    return B_Pseudo_Inv

def restricciones():
    numero_restricciones = int(input('¿Cuántas restricciones contiene tu problema?:'))
    restricciones = list()
    esEstandar=True
    variablesNB=list()
    B_aux=list()
    signoVariableNB=list()
    j=1
    restricciones_indice=0
    numero_restricciones_estandar=numero_restricciones
    LD=list()
    for i in range(numero_restricciones):
        while('s'+str(j) in variablesB):
            j+=1
        restricciones.append(re.sub(r'\s+','',input(f'Inserte la restriccion #{i+1}:')))
        B_aux.append(re.findall(r'-*[0-9]*\.*[0-9]*[a-zA-Z]+[0-9]*',restricciones[restricciones_indice]))
        LD.append([float(re.findall(r'[0-9]+$',restricciones[restricciones_indice])[0])])
        if re.search(r'[a-zA-Z]+[0-9]*=[0-9]+$',restricciones[restricciones_indice]):
            esEstandar=False
            variablesNB.append('s'+str(j))
            signoVariableNB.append(-1.0)
            B_aux.append(re.findall(r'-*[0-9]*\.*[0-9]*[a-zA-Z]+[0-9]*',restricciones[restricciones_indice]))
            LD.append([float(re.findall(r'[0-9]+$',restricciones[restricciones_indice])[0])])
            numero_restricciones_estandar+=1
            restricciones.append(restricciones[restricciones_indice])
            restricciones_indice+=1
            j+=1
        elif re.search(r'>=',restricciones[restricciones_indice]):
            esEstandar=False
            signoVariableNB.append(-1.0)
        variablesNB.append('s'+str(j))
        if len(variablesNB)-1==len(signoVariableNB):
            signoVariableNB.append(1.0)
        j+=1
        restricciones_indice+=1

    B = construirB(numero_restricciones_estandar,B_aux)
    
    B_pseudo_inv = pseudoInvB(signoVariableNB)

    cNB= [0.0 for _ in variablesNB]
    
    return np.array(B), variablesNB, np.array(cNB), np.array(B_pseudo_inv), np.array(LD), esEstandar
