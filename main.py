from modules.Construccion_matrices import funcionObjetivo, acomodarRestricciones
from modules.portada import saludo
from modules.Preparacion_final import construirTableau
from modules.simplex import simplexMatricial


import numpy as np
import pandas as pd

if __name__ == "__main__":
    saludo()
    tipo_simplex, variablesNB, cNB = funcionObjetivo()
    A, variablesB, cB, B, LD, esEstandar, ultimo_negativo = acomodarRestricciones(variablesNB)
    A, C, variablesB, variablesNB, cB, B_inv, variablesGenerales, Basicas_ubicacion, No_basicas_ubicacion = construirTableau(cB,cNB,A,B,esEstandar,ultimo_negativo,variablesB, variablesNB)
    filas = len(A)
    columnas = C.size
    Z_valor = 0
    Basicas_ubicacion,No_basicas_ubicacion,B, VNB,mensaje, Z_valor = simplexMatricial(filas, columnas, A, B_inv, cB, LD, Z_valor, C, No_basicas_ubicacion, Basicas_ubicacion)
    variablesB = list(map(lambda x: variablesGenerales[x],Basicas_ubicacion))
    variablesNB = list(map(lambda x: variablesGenerales[x],No_basicas_ubicacion))
    valoresResultado = list(map(lambda x,y: str(x)+'='+str(float(y[0])),variablesB,B))
    for i in valoresResultado:
        print(i)
    print('Z='+str(float(-1.0*Z_valor[0])))
    print(mensaje)
