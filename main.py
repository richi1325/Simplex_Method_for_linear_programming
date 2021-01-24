from modules.Construccion_matrices import funcionObjetivo, acomodarRestricciones
from modules.portada import saludo
from modules.Preparacion_final import construirTableau
from modules.simplex import simplexMatricial, simplexTesteo


import numpy as np


import os

if __name__ == "__main__":
    respuesta = 'S' 
    saludo()
    while(respuesta.upper()=='S'):
        tipo_simplex, variablesNB, cNB = funcionObjetivo()
        A, variablesB, cB, B, LD, esEstandar, ultimo_negativo = acomodarRestricciones(variablesNB)
        if len(variablesNB)==2:
            pass
            ##metodo grafico

            #cNB
            #A
            #LD
            #variablesNb
        else:
            A, C, variablesB, variablesNB, cB, B_inv, variablesGenerales, Basicas_ubicacion, No_basicas_ubicacion = construirTableau(cB,cNB,A,B,esEstandar,ultimo_negativo,variablesB, variablesNB)
            Basicas_ubicacion,No_basicas_ubicacion,VNB_valor, mensaje, z_valor, LD, iteraciones = simplexTesteo(A, B_inv, cB, LD, C, No_basicas_ubicacion, Basicas_ubicacion, esEstandar)

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
            while True:
                respuesta = input('\n\t¿Deseas resolver otro problema?[S/N]:')
                if respuesta.upper() not in ['S','N']:
                    print('\t¡Inserta una opción correcta!')
                else:
                    if respuesta.upper() == 'N':
                        print('\n\tSerá todo un placer volver a ayudarte!')
                        input('\t')
                    break
