# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 14:35:24 2020

@author: squintra
"""
##Limpieza e ingeniería de datos para clasificación de Café
##Lectura de los datos
import pandas as pd
datos = pd.read_excel('Cafe_DataCleaning.xlsx')
datos

#Descripción de los datos
#Dimensión del Dataset
datos.shape

#Tipo de variables
datos.dtypes

datos.head(5)


##Exploración de los datos
#Descripción
datos.describe()

#Exploración de datos nulos
datos.isna().sum()

#Limpieza de datos
#Variable Peso
datos['Peso'].describe()
      
#Limpieza de datos atípicos Peso
import numpy as np
datos['Peso'].std()/datos['Peso'].mean()
datos["Peso"].fillna(datos['Peso'].mean(), inplace = True)       
      

#Variable Altura
datos['Altura'].describe()
#Exploración de datos atípicos Altura
import matplotlib.pyplot as plt
plt.boxplot(datos['Altura'])
plt.title('BoxPlot altura')
plt.show()

datos['Altura'].quantile(0.95)

#Limpieza de datos atípicos
datos['Altura'][datos['Altura']>20] = datos['Altura'].mean()

#Limpieza de datos atípicos por problemas del proceso
datos['Altura'][datos['Altura']>13] = 13

datos['Altura'].quantile(0.05)

datos['Altura'][datos['Altura']<9] = 9


#Limpiar datos nulos
datos.dropna(axis=0, how = "any", inplace=True)


#Division de los datos
x = datos.iloc[:,0:-1]
y = datos.iloc[:,-1:]

#One Hot Encoding
datos_d = pd.get_dummies(x)
datos_d.head(5)


#Ingeniería de características
##Feature Selection
from sklearn.feature_selection import chi2
from sklearn.feature_selection import SelectKBest
bestfeatures = SelectKBest(score_func=chi2, k=6)
fit = bestfeatures.fit(datos_d, y)

dfscores = pd.DataFrame(fit.scores_)
dfcolumns = pd.DataFrame(datos_d.columns)

featureScores = pd.concat([dfcolumns, dfscores],axis = 1)
featureScores.columns = ['Columns','Score']

featureScores
featureScores.sort_values('Score',ascending=False)


##Normalización de los datos
from sklearn.preprocessing import StandardScaler
escalar = StandardScaler()
X = escalar.fit_transform(datos_d)
X


#Análisis de componentes principales
#Cambio de variables
datos.replace({'Arabico':'Liberica'},1, inplace=True)
datos.replace({'Tipo de grano':'Arabica'},2, inplace=True)
datos.replace({'Tipo de grano':'Robusta'},3, inplace=True)
X = datos.iloc[:, :2]
Y = datos.iloc[:,-1:].values

#Gráfico 2D
plt.title('Gráfico de dispersión café')
plt.xlabel('Diámetro')
plt.ylabel('Altura')
plt.scatter(X.iloc[:, 0], X.iloc[:, 1], c=Y, cmap=plt.cm.Set1,
            edgecolor='k')
plt.show()


#PCA
X_reduced = PCA(n_components=3)
PCA_X = X_reduced.fit_transform(datos_d)


X_reduced.explained_variance_ratio_.sum()

#Gráfica 3D
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA

fig = plt.figure(1, figsize=(8, 6))
ax = Axes3D(fig, elev=-150, azim=110)

ax.scatter(PCA_X[:, 0], PCA_X[:, 1], PCA_X[:, 2], c=Y,
           cmap=plt.cm.Set1, edgecolor='k', s=100)
ax.set_title("Gráfico de dispersión iris con los 3 componentes principales")
ax.set_xlabel("PC1")
ax.w_xaxis.set_ticklabels([])
ax.set_ylabel("PC2")
ax.w_yaxis.set_ticklabels([])
ax.set_zlabel("PC3")
ax.w_zaxis.set_ticklabels([])

plt.show()



##Ejemplo IRIS
from sklearn import datasets
iris = datasets.load_iris()
df = pd.DataFrame(data= np.c_[iris['data'], iris['target']],
                     columns= iris['feature_names'] + ['target'])

df.head(5)

X = iris.data[:, :2]  # we only take the first two features.
y = iris.target

#Gráfico 2D
plt.title('Gráfico de dispersión iris')
plt.xlabel('Sepal length')
plt.ylabel('Sepal width')
plt.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Set1,
            edgecolor='k')
plt.show()

##PCA
X_reduced = PCA(n_components=3)

X_reduced.explained_variance_ratio_.sum()


#Gráfico 3D
fig = plt.figure(1, figsize=(8, 6))
ax = Axes3D(fig, elev=-150, azim=110)

ax.scatter(PCA_X[:, 0], PCA_X[:, 1], PCA_X[:, 2], c=y,
           cmap=plt.cm.Set1, edgecolor='k', s=100)
ax.set_title("Gráfico de dispersión iris con los 3 componentes principales")
ax.set_xlabel("PC1")
ax.w_xaxis.set_ticklabels([])
ax.set_ylabel("PC2")
ax.w_yaxis.set_ticklabels([])
ax.set_zlabel("PC3")
ax.w_zaxis.set_ticklabels([])

plt.show()
PCA_X = X_reduced.fit_transform(iris.data)

