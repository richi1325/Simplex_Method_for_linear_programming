from modules.Construccion_matrices import funcionObjetivo, acomodarRestricciones
from modules.portada import saludo
from modules.Preparacion_final import construirTableau
from modules.simplex import simplexRevisado
#from modules.graphic import restriccionesGrafico,intersectarRestricciones

import numpy as np
import os

if __name__ == "__main__":
    respuesta = 'S' 
    saludo()
    it=0
    while(respuesta.upper()=='S'):
        clear = lambda: os.system('cls')
        if it==1:
            clear()
        tipo_simplex, variablesNB, cNB, z, esGrafico = funcionObjetivo()
        #if esGrafico:
        #    z, restricciones,LD,Op = restriccionesGrafico(z,variablesNB)
        #    restriccionesFactibles=intersectarRestricciones(restricciones)
        #else:
        A, variablesB, cB, B, LD, esEstandar, ultimo_negativo = acomodarRestricciones(variablesNB)
        A, C, variablesB, variablesNB, cB, B_inv, variablesGenerales, Basicas_ubicacion, No_basicas_ubicacion = construirTableau(cB,cNB,A,B,esEstandar,ultimo_negativo,variablesB, variablesNB)
        Basicas_ubicacion,No_basicas_ubicacion,VNB_valor, mensaje, z_valor, LD, iteraciones = simplexRevisado(A, B_inv, cB, LD, C, No_basicas_ubicacion, Basicas_ubicacion, esEstandar)

        variablesB = list(map(lambda x: variablesGenerales[x],Basicas_ubicacion))
        variablesNB = list(map(lambda x: variablesGenerales[x],No_basicas_ubicacion))
        valoresResultadoB = list(map(lambda x,y: '\t\t'+str(x)+' = '+str(float(y[0])),variablesB,LD))
        valoresResultadoNB = list(map(lambda x: '\t\t'+str(x)+' = '+'0',variablesNB))    
        
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
        it=1