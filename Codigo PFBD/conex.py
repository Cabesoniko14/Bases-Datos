#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 11:50:20 2022

@author: javi
"""

import psycopg2
import bibBD as bd
import pandas as pd
import bibArchivos as bib
import matplotlib.pyplot as plt
import numpy as np


# Conexión
conn = psycopg2.connect(host="localhost",
    database="Clinica",
    user="postgres",
    password="basesdatos")



#Parte 1: graficación de consulta a

cadSql= "select NomProp, NomPac, Costo from Cons c, Prop p, Paciente m where m.IdProp=p.IdProp and c.IdPac=m.IdPac order by NomProp asc, Costo desc"
tuplas1 = bd.cons(conn, cadSql)

df1 = pd.DataFrame.from_records(tuplas1, columns = ['NomProp', 'NomPac', 'Costo'])
#df1[['NomProp', 'Costo']].plot('NomProp', kind = 'bar', title = 'Consulta 1', color = 'r')


#Parte 1: graficación de consulta c

cadSql2 = "Select NomProd, count(*) From Receta r, Cons c, Producto p Where p.IdProd = r.IdProd and r.IdCons = c.IdCons Group by NomProd Having count(*)>1"
tuplas2 = bd.cons(conn, cadSql2)
df2= pd.DataFrame.from_records(tuplas2, columns = ['NomProd', 'NumRecetado'])
#df2.plot(kind = 'scatter', x = 'NomProd', y = 'NumRecetado', rot = 90, color = 'y', grid = True, title = 'Consulta 2')


#Parte 1: graficación de consulta b

df3 = bib.leeDatosDF('/Users/javi/Desktop/Codigo PFBD/csv/ConsultaB.csv', header = False, nomCols = ['NomPac', 'NomMed', 'Serv'])
#df3.plot('NomPac', 'Serv', rot = 90, color = 'g', kind = 'scatter', grid = True, title = 'Consulta 3')

#Parte 1: consulta i

df4 = bib.leeDatosDF('/Users/javi/Desktop/Codigo PFBD/csv/ConsultaG.csv', header = False, nomCols = ['NomMed', 'Promedio de costo de consultas'])
#df4.plot('NomMed', 'Promedio de costo de consultas', rot = 25, kind = 'pie', title = 'Consulta 4', labels = ['Michel','Amparo','Pedro','Fernando'], figsize = (8,8))


#Parte 2: generar procesos


#Funcion 1: comisiones por médico

def comisiones(nombre):
    cadSqlCom = "select sum(costo) from cons c, med m  where c.cedprof = m.cedprof and nommed = '" + nombre +"' group by nommed"
    tupCom = bd.cons(conn, cadSqlCom)
    ingresos = tupCom[0][0]
    porc = 0
    if ingresos > 900:
        porc = 0.3
    else:
        porc = 0.1
    comision = ingresos*porc
    ing = [ingresos]
    comi = [comision]
    index = [' ']
    df = pd.DataFrame({'Ingresos': ing,'Comisión': comi}, index=index)
    df.plot.barh(stacked=True, title = "Ingresos y comisión de " + str(nombre)) 
    return "Nombre: " + nombre + "\nComisión: " + str(comision) 
    
#print(comisiones('MICHEL A. LANDEROS MARTINEZ'))
#print(comisiones('FERNANDO CORONA MONDRAGON '))


#Funcion 2

def medPac(medico):
    funCadSql = "select nompac, costo   from paciente p, med m, cons c where p.idpac = c.idpac and c.cedprof = m.cedprof and m.nommed = '"+medico+"';  "
    res = bd.cons(conn, funCadSql)
    if res == []:
        res = "El médico no ha atendido a ningun paciente, no hay grafica"
    else:
        df = pd.DataFrame.from_records(res, columns=['Paciente', 'Costo de Consulta'])
        df.plot('Paciente', kind ='bar')
    return res

#Función 3

def gastoFecha(fechaIni, fechaFin, nom):
    funCadSql = "select sum(costo) from cons c, prop p, paciente pa where c.idpac = pa.idpac and pa.idprop = p.idprop and c.FechaCons between '"+fechaIni +"' and '"+fechaFin+ "' and nomprop = '"+nom+"'"
    res = bd.cons(conn, funCadSql)
    totCadSql = "select sum(costo) from cons c, prop p, paciente pa where c.idpac = pa.idpac and pa.idprop = p.idprop and  nomprop = '"+nom+"'"
    tot = bd.cons(conn, totCadSql)
    por = [tot[0][0] , res[0][0]]
    lista =['Fuera', 'Dentro']
    df = pd.DataFrame({'Periodo': lista, 'Gasto': por})
    df.plot('Periodo', 'Gasto', kind='pie', labels = lista, title="Gastos en el periodo")
    return res[0][0]


#Función 4: 

    
def cant_med(nombre):
    cadSqlCM = "select NomProd, sum(cantidad) from med m, cons c, receta r, producto p where m.cedprof = c.cedprof and c.idcons = r.idcons and r.idprod = p.idprod and m.nommed = '" + nombre + "'  group by nomprod"
    tupCant = bd.cons(conn, cadSqlCM)
    dfcant_med = pd.DataFrame.from_records(tupCant, columns = ['Medicamento', 'Suma de cantidades'])
    lista = dfcant_med['Medicamento'].values
    return dfcant_med.plot('Medicamento', 'Suma de cantidades', kind = 'pie', labels = lista, figsize = (8,8), title = 'Cantidades de medicamentos recetados por ' + str(nombre))
        


