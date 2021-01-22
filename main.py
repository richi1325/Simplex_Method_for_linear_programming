from modules.Construccion_matrices import funcionObjetivo, acomodarRestricciones
from modules.portada import saludo
from modules.Preparacion_final import construirTableau
from modules.simplex import simplexMatricial, simplexTesteo


import numpy as np
import pandas as pd
import os

if __name__ == "__main__":
    saludo()
    tipo_simplex, variablesNB, cNB = funcionObjetivo()
    A, variablesB, cB, B, LD, esEstandar, ultimo_negativo = acomodarRestricciones(variablesNB)
    A, C, variablesB, variablesNB, cB, B_inv, variablesGenerales, Basicas_ubicacion, No_basicas_ubicacion = construirTableau(cB,cNB,A,B,esEstandar,ultimo_negativo,variablesB, variablesNB)
    filas = len(A)
    columnas = C.size
    Z_valor = 0
    
    Basicas_ubicacion,No_basicas_ubicacion,VNB_valor, mensaje, z_valor, LD, iteraciones = simplexTesteo(A, B_inv, cB, LD, Z_valor, C, No_basicas_ubicacion, Basicas_ubicacion)

    #Basicas_ubicacion,No_basicas_ubicacion,B, VNB,mensaje, Z_valor = simplexMatricial(filas, columnas, A, B_inv, cB, LD, Z_valor, C, No_basicas_ubicacion, Basicas_ubicacion)
    variablesB = list(map(lambda x: variablesGenerales[x],Basicas_ubicacion))
    variablesNB = list(map(lambda x: variablesGenerales[x],No_basicas_ubicacion))
    valoresResultadoB = list(map(lambda x,y: '\t\t'+str(x)+' = '+str(float(y[0])),variablesB,LD))
    valoresResultadoNB = list(map(lambda x: '\t\t'+str(x)+' = '+'0',variablesNB))    
   
    clear = lambda: os.system('cls')
    clear()
    
    print('\n\n\t VALOR DE LA FUNCIÓN OBJETIVO:')
    print('\n\t\t'+str(float((-1.0)**tipo_simplex*z_valor[0])),end='\n')
    print('\n\t VARIABLES BÁSICAS:\n')
    for i in valoresResultadoB:
        print(str(i))

    print('\n\t VARIABLES NO BÁSICAS:\n')
    for i in valoresResultadoNB:
        print(str(i))
    print('\n\t'+mensaje,end='\n')

    print('\n\tNO. ITERACIONES = '+str(iteraciones))
    input('\t')

