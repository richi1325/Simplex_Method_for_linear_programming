import numpy as np

def obtenerIndiceMinimo(br_yj,y_i):
	min=np.inf
	indice=0
	for i in range(np.size(br_yj)):
		if br_yj[i]<min and y_i[i]>=0:
			indice=i
			min=br_yj[i]
	return indice

def tiene_negativos(LD):
	pos=False
	for i in range(len(LD)):
		if (LD[i][0]<0.0):
			pos=True
	return pos

def simplexRevisado(A, B_inv, cB, LD, C, No_basicas_ubicacion, Basicas_ubicacion, esEstandar):
	mensaje=''
	z_valor = np.dot(cB,LD)
	LD = np.dot(B_inv,LD)
	iteraciones=0
	if not esEstandar:
		variable_artificial = max(Basicas_ubicacion)
	else:
		variable_artificial = None 
	while True:
		VNB_valor = list()
		for i in No_basicas_ubicacion:
			VNB_valor.append(np.dot(cB,A[:,i])-C[i])
		VNB_valor_max = max(VNB_valor)

		if round(VNB_valor_max,4)<=0.0:
			mensaje="Método simplex resuelto de manera exitosa"
			if round(VNB_valor_max,4)==0.0:
				mensaje="Método simplex resuelto de manera exitosa, solución degenerada"
			elif variable_artificial is not None:
				if variable_artificial in Basicas_ubicacion or tiene_negativos(LD):
					mensaje = "Método simplex terminado, solución infactible"
			break

		indice_VNB_valor = VNB_valor.index(VNB_valor_max)

		y_i = np.dot(B_inv,A[:,No_basicas_ubicacion[indice_VNB_valor]]).reshape(1,len(A))[0]

		noAcotado = list(filter(lambda x: round(x,4)>=0.0,y_i))
		
		if not noAcotado:
			mensaje = "Método simplex terminado, solución no acotada"
			break

		br_yj = list()

		for i in range(len(LD)):
			if round(y_i[i],4)>0.0:
				br_yj.append(LD[i][0]/y_i[i])
			else:
				br_yj.append(np.inf)
		br_yj = np.array(br_yj)

		indice_min_br_yj = obtenerIndiceMinimo(br_yj,y_i)

		B_inv[indice_min_br_yj,:] = B_inv[indice_min_br_yj,:]/y_i[indice_min_br_yj]
		LD[indice_min_br_yj][0] = LD[indice_min_br_yj][0]/y_i[indice_min_br_yj]

		for i in [i for i in range(len(y_i)) if i!=indice_min_br_yj]:
			B_inv[i,:] = B_inv[i,:] - B_inv[indice_min_br_yj,:]*y_i[i]
			LD[i][0] = LD[i][0]-LD[indice_min_br_yj][0]*y_i[i]
		cB = cB-B_inv[indice_min_br_yj]*VNB_valor_max
		z_valor = z_valor-LD[indice_min_br_yj][0]*VNB_valor_max

		auxiliar_var = No_basicas_ubicacion[indice_VNB_valor]
		No_basicas_ubicacion[indice_VNB_valor] = Basicas_ubicacion[indice_min_br_yj]
		Basicas_ubicacion[indice_min_br_yj] = auxiliar_var 

		iteraciones+=1
	return Basicas_ubicacion,No_basicas_ubicacion,VNB_valor, mensaje, z_valor, LD,iteraciones
