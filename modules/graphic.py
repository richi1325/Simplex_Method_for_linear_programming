import re

def restriccionesGrafico(z,variablesNB):
    while(True):
        numero_restricciones = input('¿Cuántas restricciones contiene tu problema?:')
        x = numero_restricciones.isdigit()
        if x:
            numero_restricciones = int(numero_restricciones)
            if numero_restricciones>0:
                break
            elif numero_restricciones<=0:
                print('La cantidad no puede ser negativa o 0, intentalo de nuevo')
        else:
            print('¡Inserte una cantidad válida!')
    restricciones = list()
    z = re.sub(r'(-*[0-9]+\.*[0-9]*)([a-zA-Z]+[0-9]*)',r'\1*\2',z)
    for i in range(numero_restricciones):
        restricciones.append(re.sub(r'\s+','',input(f'Inserte la restriccion #{i+1}:')))
        restricciones[i]=re.sub(r'(-*[0-9]+\.*[0-9]*)([a-zA-Z]+[0-9]*)',r'\1*\2',restricciones[i])
    
    return z, restricciones
        