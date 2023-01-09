# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 13:46:37 2022

@author: psdist
Biblioteca para las funciones de acceso a la BD: conexión, consulta y 
actualización.
"""


#Lleva a cabo una consulta a la BD y regresa una lista con las tuplas leídas.
#Par. 1: la conexión a la BD; Par. 2: cadena de la consulta.
def cons(conex, cadSql):
  try:
    with conex.cursor() as cursor:
      cursor.execute(cadSql)
      tuplas= cursor.fetchall()
    return tuplas
  except Exception as e:
    print('\nError en consulta: ',e)
    return None

#Actualiza la BD. Se usa la misma función para dar de alta, de baja o cambiar
#tuplas en la BD.
#Par. 1: la conexión a la BD; Par. 2: cadena de la instrucción.
def actualiza(conex, cadSql):
  try:
    with conex.cursor() as cursor:
      cursor.execute(cadSql)
      print('\nÉxito en la actualización')
    return True
  except Exception as e:
    print('\nError en actualización: ',e)
    return False
  















