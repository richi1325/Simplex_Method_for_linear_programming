from modules.Construccion_matrices import funcionObjetivo, acomodarRestricciones
from modules.portada import saludo
import numpy as np

if __name__ == "__main__":
    saludo()
    variablesNB,cB = funcionObjetivo()
    B, variablesB, cNB, B_pseudo_inv, LD, esEstandar = acomodarRestricciones(variablesNB)
    print(variablesB, variablesNB)
    print(cB,cNB)
    print(B)
    print(B_pseudo_inv)
    print(LD)