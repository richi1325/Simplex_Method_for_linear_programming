import numpy as np

def construirTableau(cB, cNB, A, B, esEstandar, ultimo_negativo,variablesB, variablesNB):
    if esEstandar:
        A = np.concatenate((A,B),axis=1)
        C = np.concatenate((cNB,cB),axis=0).reshape(1,len(cB)+len(cNB))[0]
        B_inv = np.linalg.inv(B)
        variablesGenerales = variablesNB + variablesB
        Basicas_ubicacion = list(map(lambda x: variablesGenerales.index(x) ,variablesB))
        No_basicas_ubicacion = list(map(lambda x: variablesGenerales.index(x) ,variablesNB))
    
    else:
        j=97
        while('x'+chr(j) in variablesNB):
            j+=1
        
        variable_artificial = 'x'+chr(j)
        variablesGenerales = variablesNB + variablesB + [variable_artificial]

        B_artificial = list()
        for i in range(len(B)):
            B_artificial.append([1.0])
        B_artificial = np.array(B_artificial)

        big_M = float(10**(len(str(int(max(cNB))))+1))
        cB_tableau = np.concatenate((cB,[big_M]),axis=0)
        B_tableau = np.concatenate((B,B_artificial),axis=1) 
        
        #modificando elementos simplex matricial
        #variables
        variable_auxiliar = variablesB[ultimo_negativo]
        variablesB[ultimo_negativo] = variable_artificial
        variablesNB.append(variable_auxiliar)

        Basicas_ubicacion = list(map(lambda x: variablesGenerales.index(x) ,variablesB))
        No_basicas_ubicacion = list(map(lambda x: variablesGenerales.index(x) ,variablesNB))    


        #cB
        cB[ultimo_negativo] = big_M

        A = np.concatenate((A,B_tableau),axis=1)

        #B
        B[:,ultimo_negativo] = np.array(B_artificial).reshape(1,len(B_artificial)) 

        C = np.concatenate((cNB,cB_tableau),axis=0).reshape(1,len(cB_tableau)+len(cNB))[0]
        B_inv = np.linalg.inv(B)

    return A, C, variablesB, variablesNB, cB, B_inv, variablesGenerales, Basicas_ubicacion, No_basicas_ubicacion
