#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 09:22:07 2023

@author: jairoescrito
"""

# Librerías
import pandas as pd

# Carga archivos de icfes
icfes = pd.read_csv('Dataset/icfes_data.csv',sep ='\t', low_memory=False)
variables = icfes.columns
# Análisis incial conjunto de datos
#Total de columnas
len(icfes.columns)
# Total de datos
len(icfes.columns) * len(icfes)
# Total de missing values
mv = icfes.isnull().sum()
mv.sum()

# Generación de tablas

# Data estudiantes
estudiantes = icfes.iloc[:,[0,5,1,2,3,4,7,8,10,12,37,54]]
estudiantes.columns = ['Consecutivo_Est','Periodo','Tipo_Documento','Nacionalidad','Genero',
           'Fecha_Nacimiento','Pais_Residencia','Etnia','Cod_Departamento',
           'Cod_Municipio','Cod_Icfes_Colegio','Privado_Libertad']
estudiantes.to_csv('Dataset/estudiantes.csv',sep=',', index=False)

# Data estudio
estudio = icfes.iloc[:,[0,33,34,35,36]]
estudio.columns = ['Consecutivo_Est','Lectura_Diaria','Internet_Diario',
                    'Trabajo_Semanal','Tipo_Remuneración']
estudio.to_csv('Dataset/estudio.csv',sep=',', index=False)

# Data situación social
socioeconomico = icfes.iloc[:,[0,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,76,77,78]]
socioeconomico.columns = ['Consecutivo_Est','Estrato_Vivienda','Personas_Hogar','Cuartos_Hogar',
                  'Educacion_Padre','Educacion_Madre','Trabajo_Padre','Trabajo_Madre',
                  'Internet','Servicio_TV','Computador','Lavadora','Horno','Automovil',
                  'Moto','C_Videojuegos','Num_Libros','Leche_Derivados','Carne_Pescado_Huev',
                  'Cerela_Frutos_Legum','Percepcion_Econo','Ind_Situacion_Ec','Nivel_Socioecon',
                  'Nivel_Sociecon_Colegio']
socioeconomico.to_csv('Dataset/socioeconomico.csv',sep=',', index=False)

# Data resultados prueba
resultados = icfes.iloc[:,[0,58,55,5,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73,74,75]]
resultados.columns = ['Consecutivo_Est','Cod_Departamento','Cod_Municipio','Periodo',
                  'Lectura_Critica_LC','Percentil_LC', 'Desempeño_LC', 
                  'Matematicas_Mat', 'Percentil_Mat', 'Desempeño_Mat',
                  'C_Natuales_CN', 'Percentil_CN', 'Desempeño_CN',
                  'C_Sociales_CS', 'Percentil_CS', 'Desempeño_CS',
                  'Ingles_Ing', 'Percentil_Ing', 'Desempeño_Ing',
                  'Global', 'Percentil_Global']
resultados.to_csv('Dataset/resultados.csv',sep=',', index=False)

# Data establecimientos educativos
colegios = icfes.iloc[:,[37,52,50,38,39,40,41,42,43,44,45,46,47,48,49]]
colegios.columns = ['Cod_Colegio','Cod_Departamento','Cod_Municipio','Cod_DANE',
                    'Nombre_Colegio','Genero_Colegio','Naturaleza','Calendario','Bilingue',
                    'Caracter','Cod_DANE_sede','Nombre_Sede','Principal','Ubicacion','Jornada']
colegios = colegios.drop_duplicates()
colegios.to_csv('Dataset/colegios.csv',sep=',', index=False)


# Data ubicación

ubicacion = icfes.iloc[:,[10,9,12,11]] # Extraer datos de ubicación del dataset original
ubicacion.columns = ['Cod_Departamento','Departamento', # Ajustar los nombres
                     'Cod_Municipio', 'Municipio']
ubicacion = ubicacion.drop_duplicates() # Eliminar duplicados
ubicacion = ubicacion.sort_values(by = 'Cod_Municipio')
ubicacion.dropna(inplace = True, how = 'all')
ubicacion.Departamento = ubicacion.Departamento.str.title()
ubicacion.Municipio = ubicacion.Municipio.str.title()

# El merge con el df estudiantes está generando inconsistencias
len(ubicacion.Municipio.unique()) # 1034 municipios únicos frente a 1120 de la lista, esto es válido porque hay municipios con el mismo nombre
len(ubicacion.Cod_Municipio.unique()) # 1119 municipios únicos frente a 1120 de la lista, deberían ser exactamente los mismos, hay dos municipios con el mismo código
ubicacion.Municipio = ubicacion.Municipio.astype('category')
ubicacion.Municipio.info()
ubicacion.Municipio.describe()
ubicacion.Cod_Municipio = ubicacion.Cod_Municipio.astype('category')
ubicacion.Cod_Municipio.info()
ubicacion.Cod_Municipio.describe() # El muncipio con código 11001 está repetido
ubicacion.Cod_Municipio.index[ubicacion.Cod_Municipio == 11001] # Filas de las dos ubicaciones
ubicacion.loc[ubicacion.Cod_Municipio.index[ubicacion.Cod_Municipio == 11001][0]]
ubicacion.loc[ubicacion.Cod_Municipio.index[ubicacion.Cod_Municipio == 11001][1]] # Existen dos formas diferentes en las que está escrita Bogotá en el departamento




data_Colombia = pd.read_csv('Dataset/Colombia_2023.csv',thousands= '.')# Leer base de datos municipios que incluye regiones
data_Colombia.columns = ['Region','Cod_Departamento','Departamento',
                     'Cod_Municipio', 'Municipio' ]
regiones = data_Colombia.iloc[:,[0,1]].drop_duplicates()

ubicacion = ubicacion.merge(regiones, on = 'Cod_Departamento', how = 'left') # Incluir dato de regiones
ubicacion.Departamento = ubicacion.Departamento.str.title()
ubicacion.Municipio = ubicacion.Municipio.str.title()
ubicacion.isnull().sum()
ubicacion = ubicacion.dropna(how='all')
ubicacion.iloc[ubicacion.index[ubicacion['Region'].isna()],4] = 'Extranjero'


ubicacion.to_csv('Dataset/ubicacion.csv',sep=',', index=False)


