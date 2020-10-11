# -*- coding: utf-8 -*-
"""

@author: luiggi Silva Atto
Contacto: Luiggi11.16@gmail.com

Proceso de automatizacion de datos utilizando Gsheets+Scraping
"""

###############################################################################

######### Proceso automatico de generacion de reportes Covid ##################

###############################################################################

#### Pasos a seguir ##########################################################
#1.-Identificar las fuentes de información
#2.-Limpiar y estructurar las bases de datos
#3.-Crear usuarios de google developer
#4.-Carga la informacion de una hoja gshets

## Carga de paquetes ##########################################################

import os ## Paquete funciones sistema
os.chdir('C:/Users/luigg/OneDrive/Documentos/DSRP') ### Area de Trabajo
## pip install pandas ## instalar desde el cmd
## conda install pandas ## Instalar por anaconda promp

import pandas as pd ### Paquete de manejos de bases de datos

## pip install pygsheets ## instalar desde el cmd
import pygsheets ### Paquete para utilizar gsheets

### Importamos la data del portal de JHU CSSE COVID-19 Dataset################

## Para mas informacion entra a la pagina ####################################

##1.-Identificar las fuentes de información
##:https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data

##2.-Limpiar y estructurar las bases de datos
#Confirmed
Confirmed=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
Confirmed=Confirmed.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'])
Confirmed.columns=['Provincia', 'Pais', 'Lat', 'Long', 'Fecha', 'Confirmados']
Confirmed['Fecha']=pd.to_datetime(Confirmed['Fecha'],format='%m/%d/%y')
Confirmed=Confirmed.groupby(['Pais', 'Fecha'])['Confirmados'].sum().reset_index()
#Death
Deaths=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
Deaths=Deaths.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'])
Deaths.columns=['Provincia', 'Pais', 'Lat', 'Long', 'Fecha', 'Muertes']
Deaths['Fecha']=pd.to_datetime(Deaths['Fecha'],format='%m/%d/%y')
Deaths=Deaths.groupby(['Pais', 'Fecha'])['Muertes'].sum().reset_index()
#Recovered
Recovered=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
Recovered=Recovered.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'])
Recovered.columns=['Provincia', 'Pais', 'Lat', 'Long', 'Fecha', 'Recuperados']
Recovered['Fecha']=pd.to_datetime(Recovered['Fecha'],format='%m/%d/%y')
Recovered=Recovered.groupby(['Pais', 'Fecha'])['Recuperados'].sum().reset_index()

#Consolidado
data=Confirmed.merge(Deaths,how='outer',on=['Pais', 'Fecha'])
data=data.merge(Recovered,how='outer',on=['Pais', 'Fecha'])
data['Confirmados']=data['Confirmados'].fillna(0)
data['Recuperados']=data['Recuperados'].fillna(0)
data['Muertes']=data['Muertes'].fillna(0)

## Reporte Diario
import datetime as dt
diario=pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/' +(dt.date.today()-dt.timedelta(1)).strftime("%m-%d-%Y") +'.csv')
##3.-Crear usuarios de google developer
##############################################################################
################ Crear un usuario  ###########################################
##########https://console.developers.google.com/apis##########################

#### bot-751@primordial-arc-292012.iam.gserviceaccount.com####

### Import Json con los credenciales #########################################

###4.-Carga la informacion de una hoja gshets

##Historico
gc = pygsheets.authorize(service_file='json-clave.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1SXQR0t-6_g_rac2P9ixVVk6OWcsGXSpqYzL9rPVB-hs/edit#gid=0')
wks = sh[0]
wks.clear(start='A1', end=None)   
wks.set_dataframe(data, 'A1')

##diario
gc = pygsheets.authorize(service_file='C:/Users/luigg/OneDrive/Documentos/DSRP/json-clave.json')
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1PwVdgw9JXCaQn2iMD7MKpzRo_G2RfRYoSFSDuJWjnEU/edit#gid=0')
wks = sh[0]
wks.clear(start='A1', end=None)   
wks.set_dataframe(diario, 'A1')
