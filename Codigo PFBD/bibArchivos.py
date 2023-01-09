# -*- coding: utf-8 -*-
"""
@author: flopezg
Biblioteca para funciones de lectura/escritura de datos con pandas.
"""
import pandas as pd

"""
Lee n series desde un archivo de entrada.
La 1a. col. del archivo contiene a los índices.
De la 2a. columna en adelante están los valores para las n series.
"""
def leeVariasSeries(archivo, n):
	flec= open(archivo,'r')
	índices=[]
	valores= []		#Será una lista de listas vacías.
	for i in range(n):
		valores.append([])		#Crea n listas vacías, una para cada serie.

	for línea in flec:	
		datos= línea.split(",")
		índices.append(datos[0])       #Agrega a la lista de índices.
		for i in range(1,n+1):
			valores[i-1].append(float(datos[i]))#Agrega a la lista i-ésima de valores.
	flec.close()
	
	series=[]
	for i in range(n):         #Crea cada serie.
		series.append(pd.Series(valores[i],índices))
	return series

#Lee datos de un DataFrame.
#En: Archivo, hay que dar la cadena con el nombre del mismo.
def leeDatosDF(archivo,header=True,nomCols=None,índice=None):
#def leeDataFrame(archivo,header=True,nomCols=None,índice=None):
  #Lee los datos.
  if header:		#Si el archivo csv tiene encabezado.
    datos= pd.read_table(archivo, sep=',', index_col= índice)
  else:				#Si no lo tiene.
    datos= pd.read_table(archivo, sep=',', header=None,
                       names= nomCols, index_col= índice)
  return datos