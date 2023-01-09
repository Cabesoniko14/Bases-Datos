# -*- coding: utf-8 -*-
"""
Created on Fri Nov 18 14:15:58 2022

@author: psdist
Prueba de las funciones de acceso a la base de datos.
"""
import bibBD as bd
import pandas as pd
import bibArchivos as bib

#Conexión.
conex= bd.conexión('CC202-P', 'SE', 'sa', 'sqladmin21')

#Ejecución de una consulta.
cadSql= "select * from alum"
tuplas= bd.cons(conex, cadSql)
# print(tuplas)

#Prueba de insert.
# cadSql= "insert into alum values (100,'Mariana','cds',10)"
# bd.actualiza(conex, cadSql)

#Prueba de update.
# cadSql= 'update alum set prom=8 where cu=100'
# bd.actualiza(conex, cadSql)

#Prueba de delete
# cadSql= 'delete from alum where cu=100'
# bd.actualiza(conex, cadSql)

#Conversión de la tabla de resultados de la consulta a un DF.
dfAlum= pd.DataFrame.from_records(tuplas,
                                  columns=['CU','Nombre','Carrera','Prom'])
print('\n',dfAlum)

#Una consulta con group by: promedio de las materias cursadas.
cadSql= 'select nommat, avg(calif) from mater m, historial h '
cadSql += 'where m.clavem=h.clavem group by nommat'
promMat= bd.cons(conex, cadSql)
dfPromMat= pd.DataFrame.from_records(promMat, index='Materia',
                                     columns= ['Materia','Prom'])
print('\n',dfPromMat)
dfPromMat.plot(rot=40,kind='bar',grid=True)

#Cierra la BD.
conex.close()

#Consulta ejecutada en PostgreSQL cuyo resultado se guarda en una tabla nueva.
# select nomal, avg(calif) as prom
# into promAlum
# from alum a, historial h
# where a.cu=h.cu
# group by nomal

#Esa tabla nueva se exporta a un archivo csv (desde PostgreSQL):
#copy promAlum to 'C:\BD_CD\Python\BD\promAlum.csv' delimiter ',' csv header;

#Después se lee el csv creando el data frame.
dfpromAlum= bib.leeDatosDF('promAlum.csv',índice=0)
print(dfpromAlum)
dfpromAlum.plot(rot=40,kind='bar',grid=True)
















