#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 21:35:27 2023

@author: jairoescrito
"""

import pandas as pd

# Dataset estudiantes

estudiantes = pd.read_csv('Dataset/estudiantes.csv',sep =',', low_memory=False)
ubicaciones = pd.read_csv('Dataset/ubicacion.csv',sep =',', low_memory=False)
# Modificación del tipo de identificación para facilitar su entendimiento
estudiantes.Tipo_Documento = estudiantes.Tipo_Documento.replace(['CC', 'CE', 'CR', 'PC', 'PE', 'TI', 'NES', 
                                                                 'PEP', 'RC', 'CCB','NIP', 'NUIP', 'V'],
                                                                ["Cedula_Ciudadania","Cedula_Extranjeria","Otro","Otro","Otro",
                                                                 "Tarjeta_Identidad","Otro","Permiso_Esp_Permanencia","Registro_Civil",
                                                                 "Otro","Numero_Id_Personal","Numero_Unico_Id_Personal","Otro"])
estudiantes.info()
# Agregar fechas de presentación de las pruebas 
periodos = estudiantes.Periodo.unique().tolist()
fechas = ['07/11/2020','11/08/2019','10/03/2019','25/02/2018','12/08/2018','18/10/2020']
cortes = pd.DataFrame({'Periodo':periodos, 'Fecha_Prueba':fechas})
cortes.info()
estudiantes = pd.merge(estudiantes,cortes,on='Periodo',how='left') # Incluir en el dataset de estudiantes la fecha de presentación de examen
del(cortes,fechas,periodos)


# Calcular edades de los estudiantes al momento de presentación de la prueba
estudiantes.Fecha_Nacimiento.isnull().sum() # Las fechas de naciomiento no tienen nulos
estudiantes.Fecha_Prueba.isnull().sum() # Las fechas de pruebas no tienen datos nulos











# Exploración de datos de estudiantes

# Reemplazo de  siglas para facilitar entendimiento


# Dataset con la inclusión de los nombres de las ubicaciones geográficas
estudiantes['Cod_Municipio'] = estudiantes['Cod_Municipio'].astype('category')
ubicacion['Cod_Municipio'] = ubicacion['Cod_Municipio'].astype('category')

data_est = pd.merge(estudiantes,ubicacion, on = 'Cod_Municipio', how = 'left')
ubicacion.info()
estudiantes.info()
data_est.isnull().sum()






# Dataset con la inclusión de la información del periodo de presentación de la prueba
data_est = estudiantes.merge(resultados.iloc[:,[0,3]], on = 'Consecutivo_Est', how = 'left')
temp = data_est[data_est['Region'].isna()]
temp = pd.DataFrame(data_est.columns) # dataframe temporal para acceder al nombre de las variables
data_est = data_est.iloc[:,[15,0,1,2,3,4,5,6,9,10,11,13,14]] # Reducir el conjunto de datos a columnas requeridas
# Creación de data con subgrupos de conteo de estudiantes por cada dimensión
temp = pd.DataFrame(data_est.columns)# dataframe temporal para acceder al nombre de las variables
data_est_group_I = data_est.groupby(['Periodo','Tipo_Documento',
                                     'Nacionalidad','Genero']).count().iloc[:,0].reset_index() # Agrupación, selección de columnas y eliminación de indices






data_est_group_II = data_est.groupby(['Periodo','Tipo_Documento',
                                       'Genero','Region',
                                       'Departamento','Municipio'])



