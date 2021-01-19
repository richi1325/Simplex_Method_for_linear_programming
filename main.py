from modules.Construccion_matrices import funcionObjetivo, acomodarRestricciones
import numpy as np

if __name__ == "__main__":
    tipo_simplex, variablesNB, cNB = funcionObjetivo()
    A, variablesB, cB, B, LD, esEstandar = acomodarRestricciones(variablesNB)
    print(variablesB)
    print(variablesNB)
    print(cB)
    print(cNB)
    print(A)
    print(B)
    print(LD)