import re
import numpy as np
"""
print('BIENVENIDO A ESTE PROGRAMA QUE RESUELVE PROBLEMAS DE PROGRAMACIÓN LINEAL')
while(True):
    tipo_simplex = input('¿Tu problema es de MAXIMIZAR (1) o MINIMIZAR (2)?:')
    if tipo_simplex in ['1','2']:
        tipo_simplex = int(tipo_simplex)
        break
    else:
        print('¡Inserta una opción válida!')"""

z = input('Inserta la función objetivo:')
z = re.sub(r'\s+','',z)
variablesB = re.findall(r'[0-9]*\.*[0-9]*([a-zA-Z]+[0-9]*)',z)
cB =  re.findall(r'(-*[0-9]*\.*[0-9]*)[a-zA-Z]+[0-9]*',z)
for i in range(len(cB)):
    if cB[i]=='-':
        cB[i]=-1.0
    elif cB[i]!='':
        cB[i]=float(cB[i])
    else:
        cB[i]=1.0

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
print(B_aux)

cNB = [0.0 for _ in variablesNB]

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

B_Inv=list()
posicion=0
for i in range(len(signoVariableNB)):
    aux=list()
    for j in range(len(signoVariableNB)):
        if posicion==j:
            aux.append(signoVariableNB[i])
        else:
            aux.append(0.0)
    posicion+=1
    B_Inv.append(aux)

print('VARIABLES')
print(variablesB,variablesNB)
print('VALORES DE C:')
print(np.array(cB),np.array(cNB))
print('VALORES DE B:')
print(np.array(B))
print('VALORES DE B^-1:')
print(np.array(B_Inv))
print('LADO DERECHO:')
print(np.array(LD))