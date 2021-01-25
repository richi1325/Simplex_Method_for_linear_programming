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
        
    z = input('\nInserta la función objetivo:')
    if len(re.findall(r'(-*[0-9]*\.*[0-9]*[a-zA-Z]+[0-9]*)',z))==2:
        esGrafico=True
    else:
        esGrafico=False
    z = re.sub(r'\s+','',z)
    variablesNB = re.findall(r'[0-9]*\.*[0-9]*([a-zA-Z]+[0-9]*)',z)
    cNB =  re.findall(r'(-*[0-9]*\.*[0-9]*)[a-zA-Z]+[0-9]*',z)
    for i in range(len(cNB)):
        if cNB[i]=='-':
            cNB[i]=(-1)**tipo_simplex*-1.0
        elif cNB[i]!='':
            cNB[i]=(-1)**tipo_simplex*float(cNB[i])
        else:
            cNB[i]=(-1)**tipo_simplex*1.0
    return tipo_simplex, variablesNB, np.array(cNB), z, esGrafico


def construirA(restricciones,numero_restricciones_estandar,A_aux,variablesNB):
    A = list()
    for i in range(numero_restricciones_estandar):
        A.append([0.0 for _ in range(len(variablesNB))])    

    for i in range(numero_restricciones_estandar):
        if len(A_aux[i])==len(variablesNB) and re.findall(r'-*[0-9]*\.*[0-9]*([a-zA-Z]+[0-9]*)',restricciones[i]) == variablesNB:
            for j in range(len(variablesNB)):
                if re.search(r'-+[a-zA-Z]+',A_aux[i][j]):
                    A[i][j]=-1.0
                elif re.search(r'^-*[0-9]+\.*[0-9]*',A_aux[i][j]):
                    x=re.search(r'^-*[0-9]+\.*[0-9]*',A_aux[i][j])
                    A[i][j]=float(A_aux[i][j][x.start():x.end()])
                else:
                    A[i][j]=1.0
        else:
            posicion_variables=0
            posicion_A=0
            iteracion=0
            for j in range(len(variablesNB)):
                if posicion_A>len(A_aux[i])-1:
                    if len(A[i])-1==0:
                        posicion_A=0
                    else:
                        posicion_A-=1
                x=re.search(r'[a-zA-Z]+[0-9]*$',A_aux[i][posicion_A])
                if variablesNB[posicion_variables]!=A_aux[i][posicion_A][x.start():x.end()]:
                    A[i][j]=0.0
                    posicion_variables+=1
                else:
                    if re.search(r'-+[a-zA-Z]+',A_aux[i][posicion_A]):
                        A[i][j]=-1.0
                    elif re.search(r'^-*[0-9]+',A_aux[i][posicion_A]):
                        x=re.search(r'^-*[0-9]+',A_aux[i][posicion_A])
                        A[i][j]=float(A_aux[i][posicion_A][x.start():x.end()])
                    else:
                        A[i][j]=1.0
                    posicion_variables+=1
                    posicion_A+=1
                iteracion+=1
    return A


def construirB(signoVariableNB):
    B=list()
    ultimo_negativo=False
    posicion=0
    for i in range(len(signoVariableNB)):
        aux=list()
        for j in range(len(signoVariableNB)):
            if posicion==j:
                if signoVariableNB[i]<0:
                    ultimo_negativo=posicion
                aux.append(signoVariableNB[i])
            else:
                aux.append(0.0)
        posicion+=1
        B.append(aux)
    return B, ultimo_negativo

def acomodarRestricciones(variablesNB):
    while(True):
        numero_restricciones = input('¿Cuántas restricciones contiene tu problema?:')
        x = numero_restricciones.isdigit()
        if x:
            numero_restricciones = int(numero_restricciones)
            if numero_restricciones>0:
                break
            else:
                print('La cantidad no puede ser negativa o 0, intentalo de nuevo')
        else:
            print('¡Inserte una cantidad válida!')
    restricciones = list()
    esEstandar=True
    variablesB=list()
    A_aux=list()
    signoVariableNB=list()
    j=1
    restricciones_indice=0
    numero_restricciones_estandar=numero_restricciones
    LD=list()
    for i in range(numero_restricciones):
        while('s'+str(j) in variablesNB):
            j+=1
        restricciones.append(re.sub(r'\s+','',input(f'Inserte la restriccion #{i+1}:')))
        A_aux.append(re.findall(r'-*[0-9]*\.*[0-9]*[a-zA-Z]+[0-9]*',restricciones[restricciones_indice]))
        LD.append([float(re.findall(r'-*[0-9]+\.*[0-9]*$',restricciones[restricciones_indice])[0])])
        if re.search(r'[a-zA-Z]+[0-9]*=[0-9]+$',restricciones[restricciones_indice]):
            esEstandar=False
            variablesB.append('s'+str(j))
            signoVariableNB.append(-1.0)
            A_aux.append(re.findall(r'-*[0-9]*\.*[0-9]*[a-zA-Z]+[0-9]*',restricciones[restricciones_indice]))
            LD.append([float(re.findall(r'-*[0-9]+\.*[0-9]*$',restricciones[restricciones_indice])[0])])
            numero_restricciones_estandar+=1
            restricciones.append(restricciones[restricciones_indice])
            restricciones_indice+=1
            j+=1
        elif re.search(r'>=',restricciones[restricciones_indice]):
            esEstandar=False
            signoVariableNB.append(-1.0)
        variablesB.append('s'+str(j))
        if len(variablesB)-1==len(signoVariableNB):
            signoVariableNB.append(1.0)
        j+=1
        restricciones_indice+=1

    A = construirA(restricciones,numero_restricciones_estandar,A_aux,variablesNB)
    
    B, ultimo_negativo = construirB(signoVariableNB)

    cB = [0.0 for _ in variablesB]
    
    A = np.array(A).reshape(numero_restricciones_estandar,len(variablesNB))
    cB = np.array(cB)
    B = np.array(B)
    LD = np.array(LD).reshape(len(LD),1)
    return A, variablesB, cB, B, LD, esEstandar, ultimo_negativo
