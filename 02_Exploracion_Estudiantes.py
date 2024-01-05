#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 30 21:35:27 2023

@author: jairoescrito
"""

import pandas as pd
import numpy as np
from datetime import datetime
from dateutil.relativedelta import relativedelta
import plotly.express as px
import plotly.io as pio
pio.renderers.default='browser'

##### Dataset estudiantes #####

# Carga de datos
estudiantes = pd.read_csv('Dataset/estudiantes.csv',sep =',', low_memory=False)
ubicaciones = pd.read_csv('Dataset/ubicacion.csv',sep =',', low_memory=False)
##
# Modificación del tipo de identificación para facilitar su entendimiento
estudiantes.Tipo_Documento = estudiantes.Tipo_Documento.replace(['CC', 'CE', 'CR', 'PC', 'PE', 'TI', 'NES', 
                                                                 'PEP', 'RC', 'CCB','NIP', 'NUIP', 'V'],
                                                                ["Cedula_Ciudadania","Cedula_Extranjeria","Otro","Otro","Otro",
                                                                 "Tarjeta_Identidad","Otro","Permiso_Esp_Permanencia","Registro_Civil",
                                                                 "Otro","Numero_Id_Personal","Numero_Unico_Id_Personal","Otro"])
##
# Revisión del tipos de datos
estudiantes.info()
##
# Inclusión fechas de presentación de las pruebas 
periodos = estudiantes.Periodo.unique().tolist() # Crear una lista de los periodos de presentación de las pruebas
fechas = ['07/11/2020','11/08/2019','10/03/2019','25/02/2018','12/08/2018','18/10/2020'] # Fechas de presentación de la prueba por periodo consultadas en internet
cortes = pd.DataFrame({'Periodo':periodos, 'Fecha_Prueba':fechas}) # Data frame que relaciona las fechas con los periodos
cortes.info() # Verificar la estructura de este DF temporal
estudiantes = pd.merge(estudiantes,cortes,on='Periodo',how='left') # Incluir en el dataset de estudiantes la fecha de presentación de examen
del(cortes,fechas,periodos) # Eliminar variables tempporales
##
# Calculo de edades de los estudiantes al momento de presentación de la prueba
estudiantes.Fecha_Nacimiento.isnull().sum() # Las fechas de naciomiento no tienen nulos
estudiantes.Fecha_Prueba.isnull().sum() # Las fechas de pruebas no tienen datos nulos
estudiantes.Fecha_Nacimiento = pd.DataFrame(datetime.strptime(x, "%d/%m/%Y") for x in estudiantes.Fecha_Nacimiento) # Convertir fecha a datetime
estudiantes.Fecha_Prueba = pd.DataFrame(datetime.strptime(x,"%d/%m/%Y") for x in estudiantes.Fecha_Prueba) # Convertir a fecha datetime
estudiantes['Edad'] = pd.DataFrame(relativedelta(estudiantes.Fecha_Prueba[i],estudiantes.Fecha_Nacimiento[i]).years for i in range(len(estudiantes))) # Calculo de la edad
# Revisión del tipos de datos luego de los primeros ajustes
estudiantes.info()
##
# Verificación de missing values
estudiantes.isna().sum()
##
# Revisión de los datos de edades
round(estudiantes.Edad.describe(),2)
fig = px.box(estudiantes.Edad, y="Edad",
             title="Dispersión de los datos de la edad de los estudiantes")
fig
##
# Identificación de datos ilógicos
temp = estudiantes[estudiantes.Edad >= 80].index # Estudiantes con edades superiores o iguales a 80 años, índices de las filas
estudiantes.Fecha_Nacimiento[temp] = np.nan # Cambiar la fecha de nacimiento por NaN
estudiantes.Edad[temp] = np.nan # Cambiar la edad por NaN
estudiantes.isna().sum() # Verificar la cantidad de NaN
round(estudiantes.Edad.describe(),2) # Resumen de los datos
temp = estudiantes[estudiantes.Edad <= 12].index # Estudiantes con edades inferiores o iguales a 12 años
estudiantes.Fecha_Nacimiento[temp] = np.nan
estudiantes.Edad[temp] = np.nan
estudiantes.isna().sum()
round(estudiantes.Edad.describe(),2)
##
# Dispersion de los datos con el ajuste de las edades 
figb = px.box(estudiantes.Edad, y="Edad",
             title="Dispersión de los datos de la edad de los estudiantes -ajustado-")
figb
##








