import re

print('BIENVENIDO A ESTE PROGRAMA QUE RESUELVE PROBLEMAS DE PROGRAMACIÓN LINEAL')
while(True):
    tipo_simplex = input('¿Tu problema es de MAXIMIZAR (1) o MINIMIZAR (2)?:')
    if tipo_simplex in ['1','2']:
        tipo_simplex = int(tipo_simplex)
        break
    else:
        print('¡Inserta una cantidad válida!')
z = input('Inserta la función objetivo:')

for i in range(z.count('-')):
    if '-' in z:
        x = z.find('-')
        z = '+'.join([z[:x],z[x:]]) 
print(z)