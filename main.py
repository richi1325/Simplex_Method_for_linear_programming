from modules.Construccion_matrices import funcionObjetivo, acomodarRestricciones
from modules.portada import saludo
from modules.Preparacion_final import construirTableau

import numpy as np
import pandas as pd

if __name__ == "__main__":
    saludo()
    tipo_simplex, variablesNB, cNB = funcionObjetivo()
    A, variablesB, cB, B, LD, esEstandar, ultimo_negativo= acomodarRestricciones(variablesNB)
    tableau, variablesB, variablesNB, cB, B_inv = construirTableau(cB,cNB,A,B,esEstandar,ultimo_negativo,variablesB, variablesNB)
    print(tableau)
    print(variablesB)
    print(variablesNB)
    print(cB)
    print(B_inv)