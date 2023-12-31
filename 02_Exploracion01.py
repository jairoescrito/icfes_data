#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 21:35:27 2023

@author: jairoescrito
"""

import pandas as pd

# Carga archivos de icfes
icfes = pd.read_csv('Dataset/icfes_data.csv',sep ='\t', low_memory=False)
variables = icfes.columns

# Creación de subconjunto de datos de estudiantes
estudiantes = icfes.iloc[:,[0,1,2,3,4,5,7,8,9,11,37,54]]








estudiantes.columns = ['Consecutivo_Est','Periodo','Tipo_Documento','Nacionalidad','Genero',
           'Fecha_Nacimiento','Pais_Residencia','Etnia','Cod_Departamento',
           'Cod_Municipio','Cod_Icfes_Colegio','Privado_Libertad']


estudiantes.Tipo_Documento = estudiantes.Tipo_Documento.replace(['CC', 'CE', 'CR', 'PC', 'PE', 'TI', 'NES', 
                                                                 'PEP', 'RC', 'CCB','NIP', 'NUIP', 'V'],
                                                                ["Cedula_Ciudadania","Cedula_Extranjeria","Otro","Otro","Otro",
                                                                 "Tarjeta_Identidad","Otro","Permiso_Esp_Permanencia","Registro_Civil",
                                                                 "Otro","Numero_Id_Personal","Numero_Unico_Id_Personal","Otro"])



estudiantes.to_csv('Dataset/estudiantes.csv',sep=',', index=False)












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



