# -*- coding: utf-8 -*-
"""Analítica- final equipo 7

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TZWjkH3upotxfaxeeZhxz-JQsL6qripJ
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import spatial 
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objs as go
from matplotlib.pyplot import figure
import seaborn as sns

from google.colab import drive
drive.mount('/content/drive')

"""## **Preparación y limpieza de datos**

### Employee survey
"""

employee_survey = pd.read_csv('/content/drive/MyDrive/Analítica 3 para dummies /bases de datos/employee_survey_data.csv')
employee_survey.head()

print(employee_survey.shape)                    
print(employee_survey.columns)                  
print(employee_survey.dtypes)

# Categorias en cada variable 
print(employee_survey['EmployeeID'].unique())
print(employee_survey['EnvironmentSatisfaction'].unique())
print(employee_survey['JobSatisfaction'].unique())
print(employee_survey['WorkLifeBalance'].unique())

employee_survey.isnull().sum()

print((employee_survey.isnull().sum().sum() / employee_survey.size)*100)# % de nulos

employee_survey2 = employee_survey.copy() #crear una copia de la base de datos

# calcular el valor medio en cada variable y redondear
EnvironmentSatisfaction_mean = round(employee_survey[['EnvironmentSatisfaction']].mean(),0)
JobSatisfaction_mean = round(employee_survey[['JobSatisfaction']].mean(),0)
WorkLifeBalance_mean = round(employee_survey[['WorkLifeBalance']].mean(),0)

# rellenar los nulos con los valores medios correspondientes a cada variable 
employee_survey2[['EnvironmentSatisfaction']] = employee_survey2[['EnvironmentSatisfaction']].fillna(EnvironmentSatisfaction_mean)
employee_survey2[['JobSatisfaction']] = employee_survey2[['JobSatisfaction']].fillna(JobSatisfaction_mean)
employee_survey2[['WorkLifeBalance']] = employee_survey2[['WorkLifeBalance']].fillna(WorkLifeBalance_mean)
employee_survey2.isnull().sum()

# convertir los datos a enteros
employee_survey2 = employee_survey2.astype(int)

employee_survey2

"""### General data"""

general_data = pd.read_csv('/content/drive/MyDrive/Analítica 3 para dummies /bases de datos/general_data.csv', sep=';')
general_data.head()

print(general_data.shape)                    
print(general_data.columns)                  
print(general_data.dtypes)

# Categorias en cada variable 
print(general_data['BusinessTravel'].unique())
print(general_data['Department'].unique())
print(general_data['EducationField'].unique())
print(general_data['Gender'].unique())
print(general_data['JobRole'].unique())
print(general_data['MaritalStatus'].unique())
print(general_data['Over18'].unique())

# cantidad de nulos 
general_data.isnull().sum()

general_data2 = general_data.copy()

# rellenar nulos en la columna 'numero de empresas en las que ha trabajado' con el valor 0 
general_data2['NumCompaniesWorked'] = general_data2['NumCompaniesWorked'].fillna(0)

# rellenar nulos con la tecnica FFILL
general_data2['TotalWorkingYears'] = general_data2['TotalWorkingYears'].ffill()

general_data2.isnull().sum().sum()

# convertir a entero 
general_data2[['NumCompaniesWorked','TotalWorkingYears']] = general_data2[['NumCompaniesWorked','TotalWorkingYears']].astype(int)

general_data2.head()

"""### Manager survey data"""

manager_survey_data = pd.read_csv('/content/drive/MyDrive/Analítica 3 para dummies /bases de datos/manager_survey_data.csv')
manager_survey_data.head()

print(manager_survey_data.shape)                    
print(manager_survey_data.columns)                  
print(manager_survey_data.dtypes)

print(manager_survey_data['JobInvolvement'].unique())
print(manager_survey_data['PerformanceRating'].unique())

manager_survey_data.isnull().sum()

manager_survey_data2= manager_survey_data.copy()

manager_survey_data2

"""### Retirement info"""

retirement_info = pd.read_csv('/content/drive/MyDrive/Analítica 3 para dummies /bases de datos/retirement_info.csv', sep=';')
retirement_info.head()

print(retirement_info.shape)                    
print(retirement_info.columns)                  
print(retirement_info.dtypes)

print(retirement_info['Attrition'].unique())
print(retirement_info['retirementType'].unique())
print(retirement_info['resignationReason'].unique())

retirement_info.isnull().sum()

retirement_info2 = retirement_info.copy()

# Rellenar nulo 
retirement_info2['resignationReason'].fillna('Sin información', inplace = True)

retirement_info2.isnull().sum()

retirement_info2['retirementDate'] = pd.to_datetime(retirement_info2['retirementDate'])
retirement_info2.dtypes

retirement_info2

"""###In time y out time """

in_time = pd.read_csv('/content/drive/MyDrive/Analítica 3 para dummies /bases de datos/in_time.csv')
in_time.head()

print(in_time.shape)                    
print(in_time.columns)                  
print(in_time.dtypes)

in_time.isnull().sum()

in_timef =in_time.copy()

in_timefi = in_timef.rename(columns={'Unnamed: 0':'EmployeeID'})
in_timef

out_time = pd.read_csv('/content/drive/MyDrive/Analítica 3 para dummies /bases de datos/out_time.csv')
out_time.head()

print(out_time.shape)                    
print(out_time.columns)                  
print(out_time.dtypes)

out_time.isnull().sum()



out_timef =out_time.copy()

out_timefi = out_timef.rename(columns={'Unnamed: 0':'EmployeeID'})
out_timefi

"""## **Unión de Bases y manipulación**"""

df= employee_survey2.merge(general_data2, on='EmployeeID', how='left').merge(manager_survey_data2, on='EmployeeID', how='left').merge(retirement_info2, on='EmployeeID', how='left')
df.head(5)

# Adicion de variable respuesta a la base de datos
df['Desertores'] = df['retirementType'].apply(lambda x: 1 if x =='Resignation' else 0)

# Variables insignificantes
# RetirementDate
print(df['EmployeeCount'].unique())
print(df['Over18'].unique())
print(df['StandardHours'].unique())
print(df['Attrition'].unique())

# eliminar variables insignificantes
df.drop(['EmployeeCount', 'Over18','StandardHours', 'Attrition', 'retirementDate'], axis=1, inplace=True)

df.columns

df.isnull().sum()

# Rellenar nulos generados por la union de las bases de datos
df['retirementType'].fillna('No aplica', inplace = True)
df['resignationReason'].fillna('No aplica', inplace = True)

df.head()

df.columns

# selección previa de varibles utiles para el problema de analitica  
df1 = df[['JobRole','MaritalStatus','EducationField','BusinessTravel','Gender', 'Age','DistanceFromHome','EmployeeID','Education', 'MonthlyIncome','NumCompaniesWorked', 'TotalWorkingYears','Desertores']]

df1.head()

"""## **Análisis exploratorio**"""

valores=df.columns.values
print(valores)

#Analísis estadístico par variables númericas
df.describe()

for i in valores:
  print(df.value_counts(i))
  print("----------------")

!pip install sweetviz

import sweetviz as sv

reporte= sv.analyze(df)
reporte.show_html()

"""### **Gráficos**"""

df.head()

base_f = df[df['Gender']=='Female'].groupby(['Desertores'])[['Gender']].count().reset_index()
total_mujeres = df[df['Gender']=='Female']['Gender'].count()
base_m = df[df['Gender']=='Male'].groupby(['Desertores'])[['Gender']].count().reset_index()
total_hombres = df[df['Gender']=='Male']['Gender'].count()

fig = px.pie(base_f, values = 'Gender', names ='Desertores',
             title= '<b>% Desercion mujeres <b>', hole = .5,
             color_discrete_sequence=px.colors.qualitative.G10,
             )

fig.update_layout(
    template = 'simple_white',
    title_x = 0.5,
    annotations = [dict(text = str(total_mujeres), x=0.5, y = 0.5, font_size = 40, showarrow = False )])
fig.show()

fig = px.pie(base_m, values = 'Gender', names ='Desertores',
             title= '<b>% Desercion hombres <b>', hole = .5,
             color_discrete_sequence=px.colors.qualitative.G10)

fig.update_layout(
    template = 'simple_white',
    title_x = 0.5,
    annotations = [dict(text = str(total_hombres), x=0.5, y = 0.5, font_size = 40, showarrow = False )])
fig.show()

base_ji = df[df['Desertores']==1].groupby(['JobInvolvement'])[['Desertores']].count().reset_index()

dic = {1:'Low',
       2:'Medium',
       3:'High',
       4:'Very High'}
base_ji['JobInvolvement'] = base_ji['JobInvolvement'].replace(dic)


# crear gráfica:
fig = px.pie(base_ji, values = 'Desertores', names ='JobInvolvement',
             title= '<b>Desercion segun el nivel de participacion<b>',
             color_discrete_sequence=px.colors.qualitative.G10)

# agregar detalles a la gráfica:
fig.update_layout(
    template = 'simple_white',
    title_x = 0.5)

fig.show()

base_jr = df[df['Desertores']==1].groupby(['JobRole'])[['Desertores']].count().sort_values('Desertores', ascending = False).reset_index()

# crear gráfica
fig = px.bar(base_jr, x = 'JobRole', y='Desertores',
             title= '<b>Desercion segun la ocupación del empleado<b>',
             color_discrete_sequence=px.colors.qualitative.G10)

# agregar detalles a la gráfica
fig.update_layout(
    template = 'simple_white',
    title_x = 0.5)

fig.show()

base_js = df[df['Desertores']==1].groupby(['JobSatisfaction'])[['Desertores']].count().reset_index()

dic = {1:'Low',
       2:'Medium',
       3:'High',
       4:'Very High'}
base_js['JobSatisfaction'] = base_js['JobSatisfaction'].replace(dic)


# crear gráfica:
fig = px.pie(base_js, values = 'Desertores', names ='JobSatisfaction',
             title= '<b>Desercion segun el nivel de satisfacción laboral<b>',
             color_discrete_sequence=px.colors.qualitative.G10)

# agregar detalles a la gráfica:
fig.update_layout(
    template = 'simple_white',
    title_x = 0.5)

fig.show()

base_ms = df[df['Desertores']==1].groupby(['Gender','MaritalStatus'])[['Desertores']].count().reset_index()
base_ms

# crear gráfica
fig = px.bar(base_ms, x = 'Gender', y='Desertores', color = 'MaritalStatus', barmode = 'group', 
             title= '<b>Deserción por estado civil y genero<b>',
             color_discrete_sequence=px.colors.qualitative.Antique)

# agregar detalles a la gráfica
fig.update_layout(
    xaxis_title = 'Genero',
    yaxis_title = 'Deserción',
    template = 'simple_white',
    title_x = 0.5)

fig.show()

df['ingresos_categoria']= pd.cut(df['MonthlyIncome'], bins  = 3)
df['ingresos_categoria'].value_counts()

df['ingresos_categoria'] = df['ingresos_categoria'].astype(str)
dic = {'(9900.1, 73390.0]':'Low',
       '(73390.0, 136690.0]':'Medium',
       '(136690.0, 199990.0]':'High'}
df['ingresos_categoria'] = df['ingresos_categoria'].replace(dic)

base_ic1 = df[df['ingresos_categoria']=='Low'].groupby(['Desertores'])[['EmployeeID']].count().reset_index()

# crear gráfica:
fig = px.pie(base_ic1, values = 'EmployeeID', names ='Desertores',
             title= '<b>Desercion segun nivel bajo de salario<b>',
             color_discrete_sequence=px.colors.qualitative.G10)

# agregar detalles a la gráfica:
fig.update_layout(
    template = 'simple_white',
    title_x = 0.5)

fig.show()

base_ic2 = df[df['ingresos_categoria']=='Medium'].groupby(['Desertores'])[['EmployeeID']].count().reset_index()

# crear gráfica:
fig = px.pie(base_ic2, values = 'EmployeeID', names ='Desertores',
             title= '<b>Desercion segun nivel medio de salario<b>',
             color_discrete_sequence=px.colors.qualitative.G10)

# agregar detalles a la gráfica:
fig.update_layout(
    template = 'simple_white',
    title_x = 0.5)

fig.show()

base_ic3 = df[df['ingresos_categoria']=='High'].groupby(['Desertores'])[['EmployeeID']].count().reset_index()

# crear gráfica:
fig = px.pie(base_ic3, values = 'EmployeeID', names ='Desertores',
             title= '<b>Desercion segun nivel alto de salario<b>',
             color_discrete_sequence=px.colors.qualitative.G10)

# agregar detalles a la gráfica:
fig.update_layout(
    template = 'simple_white',
    title_x = 0.5)

fig.show()

base_nmw = df[df['Desertores']==1].groupby(['NumCompaniesWorked'])[['Desertores']].count().sort_values('Desertores', ascending = False).reset_index()
totales_nmw = pd.DataFrame(df['NumCompaniesWorked'].value_counts()).reset_index().rename(columns ={'index':'NumCompaniesWorked','NumCompaniesWorked':'Total'})
base_con = pd.merge(base_nmw, totales_nmw, how = 'left', on = 'NumCompaniesWorked')
base_con['porcentajes']= base_con.apply(lambda x: (x['Desertores']/x['Total'])*100, axis=1)
base_con = base_con[['NumCompaniesWorked','porcentajes']].sort_values('porcentajes', ascending = False)
base_con['NumCompaniesWorked'] = base_con['NumCompaniesWorked'].astype(str)


# crear gráfica
fig = px.bar(base_con, x = 'NumCompaniesWorked', y='porcentajes',
             title= '<b>Deserción según el número de empresas trabajadas<b>',
             color_discrete_sequence=px.colors.qualitative.G10)

# agregar detalles a la gráfica
fig.update_layout(
    template = 'simple_white',
    title_x = 0.5)
fig.update_traces(marker_color=px.colors.qualitative.Alphabet[:9])
fig.update_layout(coloraxis_showscale=False)


fig.show()

base_psh = df[df['Desertores']==1].groupby(['PercentSalaryHike'])[['Desertores']].count().sort_values('Desertores', ascending = False).reset_index()
totales_psh = pd.DataFrame(df['PercentSalaryHike'].value_counts()).reset_index().rename(columns ={'index':'PercentSalaryHike','PercentSalaryHike':'Total'})
base_consolidada = pd.merge(base_psh, totales_psh, how = 'left', on = 'PercentSalaryHike')
base_consolidada['porcentajes']= base_consolidada.apply(lambda x: (x['Desertores']/x['Total'])*100, axis=1)
base_consolidada = base_consolidada[['PercentSalaryHike','porcentajes']].sort_values('porcentajes', ascending = False)
base_consolidada['PercentSalaryHike'] = base_consolidada['PercentSalaryHike'].astype(str)

# crear gráfica
fig = px.bar(base_consolidada, x = 'PercentSalaryHike', y='porcentajes',
             title= '<b>Deserción según el % de aumento salarial<b>',
             color_discrete_sequence=px.colors.qualitative.G10)

# agregar detalles a la gráfica
fig.update_layout(
    template = 'simple_white',
    title_x = 0.5)
fig.update_traces(marker_color=px.colors.qualitative.Alphabet[:9])
fig.update_layout(coloraxis_showscale=False)


fig.show()

dfexp=df.copy()
dfexp=dfexp[["TotalWorkingYears","Desertores","Gender","Education","Department","EducationField"]]
dfexp=dfexp[dfexp['Desertores']==1].groupby(['TotalWorkingYears'])[['Desertores']].count().reset_index() # agrupar por dos columnas
#dfexp["Education"]=dfexp["Education"].astype(str)
#Gráfica
fig = px.scatter(dfexp, x = 'TotalWorkingYears', y ='Desertores', title = '<b>Deserción por años de vida laboral<b>')
#Atributos
fig.update_layout(
    xaxis_title = '<b>Años de vida laboral<b>',
    yaxis_title = '<b># desertores<b>',
    template = 'simple_white',
    title_x = 0.5,)
fig.show()

base_j = df[df['Desertores']==1].groupby(['Age'])[['Desertores']].count().sort_values('Desertores', ascending = False).reset_index()

# crear gráfica
fig = px.bar(base_j, x = 'Age', y='Desertores',
             title= '<b>Deserción según la edad<b>',
             color_discrete_sequence=px.colors.qualitative.Vivid)

# agregar detalles a la gráfica
fig.update_layout(
    template = 'simple_white',
    title_x = 0.5)
fig.update_traces(marker_color=px.colors.qualitative.Alphabet[0:70])
fig.update_layout(coloraxis_showscale=False)


fig.show()

base_jg = df[df['Desertores']==1].groupby(['Gender'])[['Desertores']].count().reset_index()



# crear gráfica:
fig = px.pie(base_jg, values = 'Desertores', names ='Gender',
             title= '<b>Deserción por género<b>',
             color_discrete_sequence=px.colors.qualitative.D3)

# agregar detalles a la gráfica:
fig.update_layout(
    template = 'simple_white',
    title_x = 0.5)

fig.show()

base_rr = df[df['Desertores']==1].groupby(['resignationReason'])[['Desertores']].count().reset_index()




# crear gráfica:
fig = px.pie(base_rr, values = 'Desertores', names ='resignationReason',
             title= '<b>Motivos de deserción<b>',
             color_discrete_sequence=px.colors.qualitative.Vivid)

# agregar detalles a la gráfica:
fig.update_layout(
    template = 'simple_white',
    title_x = 0.5)

fig.show()

base_rb = df[df['Desertores']==1].groupby(['BusinessTravel'])[['Desertores']].count().reset_index()
dic = {'Travel_Rarely':'Viaja pocas veces',
       'Travel_Frequently':'Viaja frecuentemente',
       'Non-Travel':'No viaja'
       }
base_rb['BusinessTravel'] = base_rb['BusinessTravel'].replace(dic)

fig = px.pie(base_rb, values = 'Desertores', names ='BusinessTravel',
             title= '<b>Deserción y frecuencia en viajes laborales<b>',
             color_discrete_sequence=px.colors.qualitative.Pastel)

# agregar detalles a la gráfica:
fig.update_layout(
    template = 'simple_white',
    title_x = 0.5)

fig.show()

base_re = df[df['Desertores']==1].groupby(['Education'])[['Desertores']].count().reset_index()
dic = {1:'Below College',
       2:'College',
       3:'Bachelor',
       4:'Master',
       5: 'Doctor'}
base_re['Education'] = base_re['Education'].replace(dic)


fig = px.pie(base_re, values = 'Desertores', names ='Education',
             title= '<b>Deserción de acuerdo al nivel de educación<b>',
             color_discrete_sequence=px.colors.qualitative.Pastel)

# agregar detalles a la gráfica:
fig.update_layout(
    template = 'simple_white',
    title_x = 0.5)

fig.show()

dfexp=df.copy()
dfexp=dfexp[["PerformanceRating","Age","Desertores","Gender","Education","Department","EducationField"]]

# crear gráfica
dfexp1=dfexp[dfexp['Desertores']==1].groupby(['PerformanceRating', 'Age'])[['Desertores']].count().reset_index() # agrupar por dos columnas
dfexp1["PerformanceRating"]=dfexp1["PerformanceRating"].astype(str)

#Deserción de acuerdo al desempeño
fig1 = px.bar(dfexp1, x = 'Age', y='Desertores', color = "PerformanceRating", barmode = 'group', 
             title= '<b>Desempeño laboral de los desertores<b>',
             color_discrete_sequence=px.colors.qualitative.Antique)

fig1.show()

dfexp=df.copy()
dfexp=dfexp[["WorkLifeBalance","Desertores","Age","Gender","Education","Department","EducationField",'BusinessTravel',"MaritalStatus",'DistanceFromHome',"MonthlyIncome"]]
dfexp=dfexp[dfexp['Desertores']==1].groupby(['WorkLifeBalance',"Gender"])[['Desertores']].count().reset_index() # agrupar por dos columnas

#Gráfica
fig = px.scatter(dfexp, x = 'WorkLifeBalance', y ='Desertores', color= "Gender", title = '<b>Balance<b>',
           )

#Atributos
fig.update_layout(
    xaxis_title = '<b>Nivel de balance<b>',
    yaxis_title = '<b># desertores<b>',
    template = 'simple_white',
    title_x = 0.5,)
fig.show()

"""## **Transformación (one hot encoding)**




"""

df3 = df1.copy()

list_dummies = ['JobRole','MaritalStatus','EducationField','BusinessTravel', 'Gender']
df_dummies = pd.get_dummies(df3,columns=list_dummies)

df3

"""## **Estandarización**"""

from sklearn.preprocessing import StandardScaler

# Separacion de datos  
y=df_dummies.Desertores
X1= df_dummies.loc[:,~df_dummies.columns.isin(['Desertores','EmployeeID'])]

# Estandarizacion 
scaler=StandardScaler()
scaler.fit(X1)
X2=scaler.transform(X1)
X=pd.DataFrame(X2,columns=X1.columns)

"""## **Features selection**"""

from sklearn.feature_selection import SelectFromModel
from sklearn import tree 
from sklearn.ensemble import RandomForestRegressor 
from sklearn.ensemble import GradientBoostingRegressor

#funcion para seleccionar variables 
def sel_variables(modelos,X,y,threshold):
    
    var_names_ac=np.array([])
    for modelo in modelos:
        modelo.fit(X,y)
        sel = SelectFromModel(modelo, prefit=True,threshold=threshold)
        var_names= sel.get_feature_names_out(modelo.feature_names_in_)
        var_names_ac=np.append(var_names_ac, var_names)
        var_names_ac=np.unique(var_names_ac)
    
    return var_names_ac

# Modelos a evaluar 
m_rtree=tree.DecisionTreeRegressor()
m_rf= RandomForestRegressor()
m_gbt=GradientBoostingRegressor()

modelos=list([m_rtree, m_rf, m_gbt])

# Variables seleccionadas
var_names=sel_variables(modelos,X,y,threshold="1*mean")
print('variables seleccionadas: ',var_names)
print('numero de variables finales: ',var_names.shape)

# matriz con variables seleccionadas
X2=X[var_names] 
X2.info()

"""## **Algoritmos**"""

# importar 
from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import LeaveOneOut
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier  
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn import metrics
from sklearn.datasets import make_classification
from sklearn.ensemble import GradientBoostingClassifier

# Splitting the dataset into training and test set.  
X_train, X_test, Y_train, Y_test= train_test_split(X2, y, test_size= 0.33, random_state=0)

"""#### Decision Tree"""

#Fitting Decision Tree classifier to the training set  
tree = DecisionTreeClassifier(criterion='entropy', random_state=0)  
tree.fit(X_train, Y_train)  

#Predicting the test set result  
y_pred= tree.predict(X_test)

#Accuracy score
acu_tree = accuracy_score(Y_test, y_pred)
acu_tree

#Evaluacion con método Kfold cross-validation
kfld = KFold(n_splits=10, random_state=6, shuffle=True)

res = cross_val_score(tree, X2, y, cv=kfld)

res.mean()*100

#Creacion matriz de confusion 
cm_tree= confusion_matrix(Y_test, y_pred) 
cm_tree

#classification report
prediccion = tree.predict(X_test)
reporte_tree = classification_report(Y_test,prediccion)
print(reporte_tree)



"""#### Random Forest"""

#Creamos un forrest para nuestro modelo
clasificador2 = RandomForestClassifier(n_estimators=10)
#Entrenamos nuestro bosque
clasificador2 = clasificador2.fit(X2,y)

#predicciones y evaluación del modelo
cv = RepeatedStratifiedKFold(n_splits=10, n_repeats=3, random_state=1)
n_scores = cross_val_score(clasificador2, X2, y, scoring='accuracy', cv=cv, n_jobs=-1, error_score='raise')
# report performance
print('Accuracy:', (n_scores.mean()))

kfld = KFold(n_splits=10, random_state=6, shuffle=True)

modelo = RandomForestClassifier(n_estimators=10)

res = cross_val_score(modelo, X2, y, cv=kfld)

res.mean()*100

#classification report
clasificador2.fit(X_train, Y_train)
prediccion = clasificador2.predict(X_test)
reporte = classification_report(Y_test,prediccion)
print(reporte)

model =  RandomForestClassifier(n_estimators=10)
model.fit(X_train, Y_train)
predicted = model.predict(X_test)
matrix = confusion_matrix(Y_test, predicted,labels=[0,1])
print(matrix)

cm = pd.DataFrame(
    confusion_matrix(Y_test, predicted,labels=[0,1]), 
    index=['Real:{:}'.format(x) for x in [0,1]], 
    columns=['Pred:{:}'.format(x) for x in [0,1]]
)
cm

"""###Gradient boosting classifier"""

# Inicializar el clasificador de Gradient 

clf = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)

# Entrenar el clasificador con los datos de entrenamiento 

clf.fit(X_train, Y_train)

# Predecir las etiquetas de clase para los datos de prueba
y_pred = clf.predict(X_test) 

# Evaluar la precisión del modelo 

accuracy = accuracy_score(Y_test, y_pred) 
print("Precisión: {:.2f}".format(accuracy))

kfld = KFold(n_splits=10, random_state=6, shuffle=True)

res = cross_val_score(clf, X2, y, cv=kfld)

res.mean()*100

#classification report
clf.fit(X_train, Y_train)
prediccion = clf.predict(X_test)
reporte = classification_report(Y_test,prediccion)
print(reporte)

#Creacion matriz de confusion 
cm= confusion_matrix(Y_test, y_pred) 
cm

"""##**Tunning hyperparameters**"""

tree.get_params()

from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.datasets import load_iris
 
# Definir la grilla de hiperparámetros
params = {'max_depth': [10,20,40,50],
          'min_samples_split': [2, 4, 6, 8, 10],
          'min_samples_leaf': [1, 2, 3, 4, 5],
          'max_features': ['sqrt', 'log2', None],
          'criterion': ['gini', 'entropy']}

# Tecnica busqueda de rejilla

# Realizar la búsqueda de hiperparámetros
grid_search = GridSearchCV(estimator=tree, param_grid=params, scoring='recall', cv=5)
grid_search.fit(X_train, Y_train)

# Ver los mejores hiperparámetros
print(grid_search.best_score_)
print('accuracy score sin afinamiento de parametros: ',acu_tree)
print(grid_search.best_params_)

# Modelo con el afinamiento de hiperparametros
modelo_final= grid_search.best_estimator_

# prediccion de un solo sample
print(modelo_final.predict([X2.iloc[1,:]]))

"""##**Análisis del modelo**"""

#classification report

modelo_final.fit(X_train, Y_train)
prediccion = modelo_final.predict(X_test)
reporte_modelof = classification_report(Y_test,prediccion)
print('Modelo con afinamiento de hiperparametros:')
print(reporte_modelof)
#------------------------------
print('Modelo antes de afinamiento de hiperparametros:')
print(reporte_tree)

prediccion_= modelo_final.predict(X_test)

#Creacion matriz de confusion 
cm_modelof= confusion_matrix(Y_test, prediccion) 
print('Modelo con afinamiento de hiperparametros:')
print(cm_modelof)
print('Modelo antes de afinamiento de hiperparametros:')
print(cm_tree)

#Evaluación de sobre-ajuste
import joblib
from sklearn.model_selection import cross_val_predict, cross_val_score, cross_validate
import numpy as np
eval=cross_validate(modelo_final,X2,y,cv=5,scoring="accuracy",return_train_score=True)
train_rf=pd.DataFrame(eval['train_score'])
test_rf=pd.DataFrame(eval['test_score'])
train_test_rf=pd.concat([train_rf, test_rf],axis=1)
train_test_rf.columns=['train_score','test_score']
print(train_test_rf)

#Guardar el modelo en formato pkl
joblib.dump(modelo_final, "modelo_final.pkl")

#Cargar el modelo
modelo_final = joblib.load("modelo_final.pkl")

modelo_final.feature_importances_

X2.columns

"""De acuerdo con la métrica se obtiene el nivel de importancia de cada variable del modelo, se identifican algunas de gran peso, tales como: 


1. ***MonthlyIncome***, con un 0.24887 de nivel de importancia.
2. ***Age***, con un 0.17115 de nivel de importancia.
3. ***TotalWorkingYears***, con un 0.14934 de nivel de importancia.
4. ***NumCompaniesWorked***, con un 0.08417 de nivel de importancia.
5. ***Education***, con un 0.05796 de nivel de importancia.

______________________________________________________________________
1. El en análisis exploratorio, encontramos que en el ingreso mensual es un elemento clave para el proceso de selección, donde se puede definir una estrategia en donde se evalue el nivel de retribución económica que se ajuste al puesto de acuerdo con el nivel de desempeño, su rol y puede reducir la deserción. 

2. En la variable edad, se haya un nivel de importancia considerable, esto se debe a que existe la posibilidad de que en determinado rango de edad se dé un comportamiento inestable en el ámbito laboral. Se considera que las personas con menor edad, poseen mayores elementos circunstanciales como metas y objetivos que implican dicha inestabilidad. Por lo tanto, es posible por parte de RRHH evaluar y ofrecer reportes que indiquen una proyección al trabajador sobre su desarrollo al interior de la compañía. Además de fomentar programas de desarrollo (ascensos) al interior de la compañía. 

3. La cantidad de años que un trabajador sigue vinculado con la empresa depende de la edad, puesto que, una persona a mayor edad tiende a permanecer más tiempo fijo en determinado trabajo.

##**Despliegue**
"""

import openpyxl ## para exportar a excel

joblib.dump(modelo_final, "modelo_final.pkl") ## 
joblib.dump(list_dummies, "list_dummies.pkl")  ### para convertir a dummies
joblib.dump(var_names, "var_names.pkl")  ### para variables con que se entrena modelo
joblib.dump(scaler, "scaler.pkl")

#transformaciones(dummies, seleccion de variables y estandarizacion)

def preparar_datos(df):
   
    

    #######Cargar y procesar nuevos datos ######

    list_dummies=joblib.load("list_dummies.pkl")
    var_names=joblib.load("var_names.pkl")
    scaler=joblib.load( "scaler.pkl") 

    ####Ejecutar funciones de transformaciones

    df_dummies=pd.get_dummies(df,columns=list_dummies)
    df_dummies= df_dummies.loc[:,~df_dummies.columns.isin(['Desertores','EmployeeID'])]
    X2=scaler.transform(df_dummies)
    X=pd.DataFrame(X2,columns=df_dummies.columns)
    X=X[var_names]
    
    return X

##df1 base de datos de ejemplo 
df_t= preparar_datos(df1)


##Cargar modelo y predecir
modelo_final = joblib.load("modelo_final.pkl")
predicciones=modelo_final.predict(df_t)
pd_pred=pd.DataFrame(predicciones, columns=['predicciones_actuales'])

###Crear base con predicciones ####

pred_actuales =pd.concat([df['EmployeeID'],df_t,pd_pred],axis=1)

### filtrar base con 10 aspirantes en riesgo de deserción

pred_desertores = pred_actuales[pred_actuales['predicciones_actuales'] == 1].head(10).reset_index().drop(['index'],axis=1)

### tabla variables importantes 

variables = pd.DataFrame( X2.columns)
importancia = pd.DataFrame(modelo_final.feature_importances_)
importancia_variables=pd.concat([variables,importancia],axis=1)
importancia_variables.columns=["Variable","Peso"]
importancia_variables= importancia_variables.sort_values(by=["Peso"], ascending=False).reset_index().drop(['index'],axis=1)

### exportar datos a excel
pred_desertores.to_excel("prediccion.xlsx")   #### predicciones de riesgo de desercion de 10 aspirantes 
importancia_variables.to_excel("importancia_variables.xlsx") ### variables mas importantes del modelo