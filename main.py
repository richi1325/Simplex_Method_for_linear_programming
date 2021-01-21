from modules.Construccion_matrices import funcionObjetivo, acomodarRestricciones
from modules.portada import saludo
from modules.Preparacion_final import construirTableau
from modules.simplex import simplexMatricial


import numpy as np
import pandas as pd

if __name__ == "__main__":
    saludo()
    tipo_simplex, variablesNB, cNB = funcionObjetivo()
    A, variablesB, cB, B, LD, esEstandar, ultimo_negativo= acomodarRestricciones(variablesNB)
    A, C, variablesB, variablesNB, cB, B_inv, variablesGenerales, Basicas_ubicacion, No_basicas_ubicacion = construirTableau(cB,cNB,A,B,esEstandar,ultimo_negativo,variablesB, variablesNB)

    Z_valor = 0
    
    #C
    print(C)
    #Matriz restricciones
    print(A)
    filas = len(A)
    columnas = C.size
    #Todas las variables
    print(variablesGenerales)
    print(Basicas_ubicacion, No_basicas_ubicacion)
    #ZR
    print(cB)
    #MR
    print(B_inv)
    #B
    print(LD)   
    
    simplexMatricial(filas, columnas, A, B_inv, cB, LD, Z_valor, C, No_basicas_ubicacion, Basicas_ubicacion)