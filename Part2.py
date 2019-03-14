# -*- coding: utf-8 -*-
"""
Created on Sat Oct 27 16:02:39 2018

@author: arpan
"""


import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="Arpan",
  passwd="root123",database="world"
)



import pandas as pd

city=pd.read_sql("SELECT * FROM city;",mydb) #Loads everything from city
country=pd.read_sql("SELECT * FROM country;",mydb) #Loads evrything from country 
countrylanguage=pd.read_sql("SELECT * FROM countrylanguage;",mydb)

#Q1.
# Prints all coloums of top 10 countries with highest population( and also above 50000000)
sql_q1=pd.read_sql("select * from country where population > 50000000 order by population DESC limit 10",mydb)
pandas_q1=country.loc[country['Population']>50000000,:].sort_values('Population',ascending=False,inplace=False).head(10)

#Q2.
#Prints number of countries and total popoulation for each continent and orders it by number of countries
sql_q2=pd.read_sql("select Continent, count(*) As Number_Countries, sum(population) As Population from country where population > 0 group by Continent order by 1 ASC",mydb)
pandas_q2=country.loc[country['Population']>0,:].groupby('Continent',as_index=False).agg({'Population':sum,'Code':len})
pandas_q2.rename(columns={'Code':'Number_Countries'},inplace=True)
pandas_q2=pandas_q2[['Continent','Number_Countries','Population']]

#Q3
# Prints name of top 10 cities with most population of USA 
sql_q3=pd.read_sql("select city.Name As City, city.population from city inner join country ON city.CountryCode = country.code where country.code = 'USA' order by city.population DESC limit 10",mydb)
pandas_q3=city.loc[city['CountryCode'].isin(country.loc[country['Code']=='USA','Code']),['Name','Population']].sort_values('Population',ascending=False,inplace=False).head(10)
pandas_q3.rename(columns={'Name':'City'},inplace=True)

#Q4
# Prints countries and number of people who speak the offical language for that country for top 10 countries with maximum people who speak the official language 
sql_q4=pd.read_sql("select country.Name, Language, (Percentage * population) / 100 from countrylanguage inner join country on countrylanguage.CountryCode = country.code where IsOfficial = True order by 3 DESC limit 10",mydb)
pandas_q4=pd.merge(countrylanguage.loc[countrylanguage['IsOfficial']=='T',:],country[['Name','Code','Population']],how='inner',left_on='CountryCode',right_on='Code')
pandas_q4['(Percentage * population) / 100']=pandas_q4['Population']*pandas_q4['Percentage']/100
pandas_q4=pandas_q4.sort_values('(Percentage * population) / 100',ascending=False,inplace=False).head(10)[['Name','Language','(Percentage * population) / 100']]

#Q5
#Prints Top 5 Languages spoken in the world with the number of people who speak it 
sql_q5=pd.read_sql("select Language, sum((Percentage * population) / 100)from countrylanguage inner join country ON countrylanguage.CountryCode = country.code group by Language order by 2 desc limit 5",mydb)
pandas_q5t=pd.merge(countrylanguage[['CountryCode','Language','Percentage']],country[['Population','Code']],how='inner',left_on='CountryCode',right_on='Code')
pandas_q5t['(Percentage * population) / 100']=pandas_q5t['Population']*pandas_q5t['Percentage']/100
pandas_q5=pandas_q5t.groupby('Language',as_index=False).agg({'(Percentage * population) / 100':sum})
pandas_q5=pandas_q5.sort_values('(Percentage * population) / 100',ascending=False,inplace=False).head(5)[['Language','(Percentage * population) / 100']]
