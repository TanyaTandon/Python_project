# -*- coding: utf-8 -*-
"""
Created on Sun Nov  4 14:04:34 2018

@author: arpan
"""
import os
import glob
import pandas as pd
import matplotlib.pyplot as plt

path='C:/Users/arpan/OneDrive/Desktop/Acads/Java & Python/HW/Project1/Names of State'

class BabyNames():
    def __init__(self,path):
        os.chdir(path)
        files=glob.glob('*.txt')
        master=pd.DataFrame()
        for file in files:
            df=pd.read_table(file,delimiter=',',header=None)
            df.columns=['State','Gender','Year','Name','Frequency']
            master=pd.concat([master,df],axis=0)
        self.master=master       

    def count_func(self,state='',year=''):
        master=self.master
        if state=='' and year=='':
            subset=master.copy()
            output=pd.DataFrame({'Geography':'Overall','Year':'Overall','Total_Births':subset['Frequency'].sum()},index=[0])
        elif year=='':
            subset=master.loc[master['State']==state,:]
            output=pd.DataFrame({'Geography':state,'Year':'Overall','Total_Births':subset['Frequency'].sum()},index=[0])
        elif state=='':
            subset=master.loc[master['Year']==year,:]
            output=pd.DataFrame({'Geography':'Overall','Year':year,'Total_Births':subset['Frequency'].sum()},index=[0])        
        else:
            subset=master.loc[((master['State']==state) & (master['Year']==year)),:]
            output=pd.DataFrame({'Geography':state,'Year':year,'Total_Births':subset['Frequency'].sum()},index=[0]) 
        print(output.to_string(index=False)) 
        
    def top_baby_names(self,state='',year=''):
        master=self.master
        if state=='' and year=='':
            subset=master.copy()
        elif year=='':
            subset=master.loc[master['State']==state,:]
        elif state=='':
            subset=master.loc[master['Year']==year,:]
        else:
            subset=master.loc[((master['State']==state) & (master['Year']==year)),:]
        subset_fem=subset.loc[subset['Gender']=='F',:]
        subset_male=subset.loc[subset['Gender']=='M',:]
        subset_fem=subset_fem.groupby('Name',as_index=False).agg({'Frequency':sum}).sort_values('Frequency',ascending=False).head(10)
        subset_male=subset_male.groupby('Name',as_index=False).agg({'Frequency':sum}).sort_values('Frequency',ascending=False).head(10)
        rank=[i for i in range(1,11)]
        output=pd.DataFrame({'Rank':rank,'Female':subset_fem['Name'].tolist(),'Male':subset_male['Name'].tolist()})
        print(output.to_string(index=False))        

    def change_popularity(self,from_year,to_year,top):
        master=self.master
        from_data=master.loc[master['Year']==from_year]
        to_data=master.loc[master['Year']==to_year]
        from_data_summ=from_data.groupby('Name',as_index=False).agg({'Frequency':sum})
        from_data_summ['Popularity']=from_data_summ['Frequency']/sum(from_data_summ['Frequency'])
        to_data_summ=to_data.groupby('Name',as_index=False).agg({'Frequency':sum})
        to_data_summ['Popularity']=to_data_summ['Frequency']/sum(to_data_summ['Frequency'])
        
        compare_data=pd.merge(from_data_summ,to_data_summ,how='inner',on='Name')
        compare_data['Popularity_Change']=(compare_data['Popularity_y']/compare_data['Popularity_x']-1)*100
        compare_data['No_change']=abs(compare_data['Popularity_Change']-0)
        
        print("Top {} names with increase in popularity".format(top))    
        print(compare_data.sort_values('Popularity_Change',ascending=False)[['Name']].head(top).to_string(index=False))
        print("Top {} names with decrease in popularity".format(top))    
        print(compare_data.sort_values('Popularity_Change')[['Name']].head(top).to_string(index=False))
        print("Top {} names with minimum change in popularity".format(top))    
        print(compare_data.sort_values('No_change')[['Name']].head(top).to_string(index=False))
    
    def change_popularityv2(self,from_year,to_year,top):
        master=self.master
        from_data=master.loc[master['Year']==from_year]
        to_data=master.loc[master['Year']==to_year]
        from_data_summ=from_data.groupby(['Name','Gender']).agg({'Frequency':sum})
        from_data_summ=from_data_summ.groupby(level=1).apply(lambda x:100*x/float(x.sum())).reset_index()   

        to_data_summ=to_data.groupby(['Name','Gender']).agg({'Frequency':sum})
        to_data_summ=to_data_summ.groupby(level=1).apply(lambda x:100*x/float(x.sum())).reset_index() 

#        to_data_summ['Popularity']=to_data_summ['Frequency']/sum(to_data_summ['Frequency'])
        
        compare_data=pd.merge(from_data_summ,to_data_summ,how='inner',on=['Name','Gender'])
        compare_data['Popularity_Change']=(compare_data['Frequency_y']/compare_data['Frequency_x']-1)*100
        compare_data['No_change']=abs(compare_data['Popularity_Change']-0)
        
        print("Top {} names with increase in popularity".format(top))    
        print(compare_data.sort_values('Popularity_Change',ascending=False)[['Name','Gender']].head(top).to_string(index=False))
        print("Top {} names with decrease in popularity".format(top))    
        print(compare_data.sort_values('Popularity_Change')[['Name','Gender']].head(top).to_string(index=False))
        print("Top {} names with minimum change in popularity".format(top))    
        print(compare_data.sort_values('No_change')[['Name','Gender']].head(top).to_string(index=False))
    

    def top5names(self,year,sex=''):
        master=self.master
        if sex=='':
            subset=master.loc[master['Year']==year,:]
        else:
            subset=master.loc[((master['Year']==year) & (master['Gender']==sex)),:]
        
        summary=subset.groupby(['State','Name'],as_index=False).agg({'Frequency':sum}) 
        summary.sort_values(['State','Frequency'],inplace=True,ascending=[True,False])   
        
        State,Rank1,Num1,Rank2,Num2,Rank3,Num3,Rank4,Num4,Rank5,Num5=([] for i in range(11))
        for i in summary['State'].unique():
            temp=summary.loc[summary['State']==i,:].head(5).unstack()
            for a,b in enumerate([Rank1,Rank2,Rank3,Rank4,Rank5]):
                b.append(temp['Name'].iloc[a])
            for a,b in enumerate([Num1,Num2,Num3,Num4,Num5]):
                b.append(temp['Frequency'].iloc[a])
            State.append(i)
        output=pd.DataFrame({'State':State,'Rank1':Rank1,'Num1':Num1,'Rank2':Rank2,'Num2':Num2,'Rank3':Rank3,'Num3':Num3,'Rank4':Rank4,'Num4':Num4,'Rank5':Rank5,'Num5':Num5})
        print(output)  

    def name_popularity(self,name,yearRange,state,sex):
        master=self.master
        subset=master.loc[((master['State']==state) & (master['Gender']==sex))]
        subset=subset.loc[((subset['Year']>=yearRange[0]) & (subset['Year']<=yearRange[1]))][['Year','Name','Frequency']]
        subset.set_index(['Year','Name'],inplace=True)
        subset=subset.groupby(level=0).apply(lambda x:100*x/float(x.sum())).reset_index()
        to_data_summ=to_data_summ.groupby(level=1).apply(lambda x:100*x/float(x.sum())).reset_index()
        name_data=subset.loc[subset['Name']==name]
        if len(name_data)==0:
            print("Name not available in the Range")
        else:
            Popularity=pd.DataFrame({'Year':[i for i in range(yearRange[0],yearRange[1])]})
            Popularity=pd.merge(Popularity,name_data[['Year','Frequency']],how='left').sort_values('Year')
            fig,ax=plt.subplots()
            ax.plot(Popularity['Year'],Popularity['Frequency'])
            ax.set_xlabel('Year')
            ax.set_ylabel('Popularity (%)')
            plt.title("Name "+name+' Popuarity Trend in '+state+" during "+str(yearRange[0])+"-"+str(yearRange[1]))

    def name_flip(self,n=10):
        master=self.master
        common_names=master.loc[((master['Gender']=='F') & (master['Name'].isin(master.loc[master['Gender']=='M','Name'].unique().tolist()))),'Name'].unique().tolist()
        subset=master.loc[master['Name'].isin(common_names)]
        subset_summ=pd.pivot_table(data=subset,index=['Name','Year'],columns='Gender',values='Frequency',aggfunc=sum).reset_index()   
        subset_total=subset.groupby('Name',as_index=False).agg({'Frequency':sum}).sort_values('Frequency')
    
    #Create a cartesian table
        year_unique=subset_summ[['Year']].drop_duplicates('Year')
        year_unique['temp']=1
        name_unique=subset_summ[['Name']].drop_duplicates('Name')
        name_unique['temp']=1
        cross_table=pd.merge(year_unique,name_unique,on='temp').drop('temp',axis=1)
        cross_table=pd.merge(cross_table,subset_summ,on=['Year','Name'],how='left').fillna(0)
        cross_table['Indicator']=[1 if x>y else 0 if x==y else -1 for x,y in zip(cross_table['F'],cross_table['M'])]
        flip=pd.pivot_table(cross_table,index='Name',columns='Indicator',values='Year',aggfunc=len).reset_index().fillna(0)
        flip['flip_Indicator']=[1 if (x>0 and y>0) else 0 for x,y in zip(flip.iloc[:,1],flip.iloc[:,3])]
        flipped=pd.merge(flip.loc[flip['flip_Indicator']==1,:],subset_total[['Name','Frequency']],on='Name').sort_values('Frequency',ascending=False)
        plot_data=cross_table.loc[cross_table['Name'].isin(flipped.head(n)['Name'])].sort_values(['Name','Year'])
        for i,name in enumerate(flipped.sort_values('Frequency',ascending=False).head(n)['Name'].unique().tolist()):
            temp_data=plot_data.loc[plot_data['Name']==name]
            fig,ax=plt.subplots()
            ax.plot(temp_data['Year'],temp_data['F'],label='Female')
            ax.plot(temp_data['Year'],temp_data['M'],label='Male')
            ax.set_xlabel('Year')
            ax.set_ylabel('Frequency')
            plt.title("Name "+name+' Flip_Trend')
            plt.legend(loc='upper left')

    def story(self):
        master=self.master
        master['Vowel_Flag']=[1 if x[0] in (['A','E','I','O','U']) else 0 for x in master['Name']]
        temp=pd.pivot_table(data=master,index=['Year','Gender'],columns='Vowel_Flag',values=['Frequency'],aggfunc=sum).reset_index() 
        temp.columns=['Year','Gender','Frequency_Non_V','Frequency_V']
        temp['Vowel_Proportion']=100*round(temp['Frequency_V']/(temp['Frequency_V']+temp['Frequency_Non_V']),3)
        temp.sort_values('Year',inplace=True)
        fig,ax=plt.subplots()
        ax.plot(temp.loc[temp['Gender']=='F','Year'],temp.loc[temp['Gender']=='F','Vowel_Proportion'],label='Female')
        ax.plot(temp.loc[temp['Gender']=='M','Year'],temp.loc[temp['Gender']=='M','Vowel_Proportion'],label='Male')
        ax.set_xlabel('Year')
        ax.set_ylabel('Percentage (%)')
        plt.title('Proportion of Names starting with a Vowel')
        plt.legend(loc='upper left')                      