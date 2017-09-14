
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[2]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Project - Hypothesis Testing to compare the mean price of house in a University Towns before the recession began and at the recession bottom.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this project:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 

# In[1]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 
          'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 
          'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 
          'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'PR': 'Puerto Rico',
          'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 
          'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 
          'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'DC': 'District of Columbia',
          'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 
          'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 
          'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 
          'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 
          'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 
          'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}

#'PR': 'Puerto Rico','DC': 'District of Columbia', 
States = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware',
          'Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky',
          'Louisiana','Maine', 'Maryland','Massachusetts','Michigan','Minnesota','Mississippi',
          'Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico',
          'New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania',
          'Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont',
          'Virginia','Washington','West Virginia','Wisconsin','Wyoming']
# In[63]:

import pandas as pd
import numpy as np
import copy as cp
def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    #data = pd.read_('university_towns.txt', sep=" ", header = None)
    data = []
    with open ('university_towns.txt', "r") as myfile:
        data.append(myfile.readlines())
    df = pd.DataFrame(data)
    df = df.transpose()
    df.replace(regex=True,inplace=True,to_replace=r"\s*\(.*\n",value=r"")
    df.replace(regex=True,inplace=True,to_replace=r"\[.*\n",value=r"")
    df.replace(regex=True,inplace=True,to_replace=r"\n",value=r"")
    df.replace(regex=True,inplace=True,to_replace=r"\s*$",value=r"")
    df = df.values.tolist()
    st = list(States)
    df2 = list()
    s=''
    df3=list()
    sta = []
    for i in df:
        i = i[0]
        flag = 0
        for j in st:
            if i == j:
                if i not in sta:
                    sta.append(i)
                    flag = 1
                    s = i
                    if len(df3)==1:
                        df3.pop()
                    elif len(df3)==2:
                        df3.pop()
                        df3.pop()
                break
        if flag == 1:
            df3.append(s)
        else:
            if len(df3)==1:
                df3.append(i)
        if flag != 1:
            df3_1=[]
            df3_1 = cp.copy(df3)
            df2.append(df3_1)
            df3.pop()
    df2 = pd.DataFrame(df2, columns=["State", "RegionName"])

    
    #rgn_loc = (33, 218, 237, 442)
    #rgn_loc = (184, 217)
    #print(df2.loc[rgn_loc,'RegionName'])
    #print(df2[df2["RegionName"]=='Los Angeles'])
    #print(df)
    #df2.set_index("State",inplace=True)
    #df3 = df2.set_index("State").groupby(level=0)['RegionName']
    #df5.append()
    #print(df2.iloc[420:440])
    #print(len(df2))
    return df2
get_list_of_university_towns()


# In[3]:

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    data = pd.read_excel('gdplev.xls', sep=" ", header = None,skiprows=220)
    data1=data.ix[:,5]
    rec_start = ""
    rec_start_ind = 890000#Random number > len(data1)
    for i in range(len(data1)-2):
        if(data1[i] > data1[i+1]) and (data1[i+1]>data1[i+2]):
                rec_start_ind = i
                break
    return data.iloc[rec_start_ind][4]
get_recession_start()


# In[4]:

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    data = pd.read_excel('gdplev.xls', sep=" ", header = None,skiprows=220)
    data1=data.ix[:,5]
    rec_start = ""
    rec_start_ind = 890000#Random number > len(data1)
    for i in range(len(data1)-2):
        if(data1[i] > data1[i+1]) and (data1[i+1]>data1[i+2]):
                rec_start_ind = i
                break
    start_yr = get_recession_start()
    data = pd.read_excel('gdplev.xls', sep=" ", header = None,skiprows=220)
    ind = data[data.ix[:,4]==start_yr].index.values[0]
    data1=data.ix[:,5]
    rec_start = ""
    rec_end_ind = 0
    for i in range(rec_start_ind,len(data1)-2):
        if(data1[i] < data1[i+1]) and (data1[i+1]<data1[i+2]):
                rec_end_ind = i+2
                break
    return data.iloc[rec_end_ind][4]
get_recession_end()


# In[5]:

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    data = pd.read_excel('gdplev.xls', sep=" ", header = None,skiprows=220)
    st = data[data.ix[:,4]==get_recession_start()].index.values[0]
    end = data[data.ix[:,4]==get_recession_end()].index.values[0]
    data1=data.iloc[st:end+1]
    data1 = data1.ix[:,5]
    minm = np.min(data1)
    a = data[data.ix[:,5]==minm].ix[:,4].tolist()
    return a[0]
get_recession_bottom()


# In[22]:

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    data = pd.read_csv('City_Zhvi_AllHomes.csv', sep=",", header = None)
    data.columns = data.iloc[0]
    data = data[1:]
    #data.set_index(["State","RegionName"],inplace=True)
    #print(data)
    data1 = data.ix[:,"State"]
    k = []
    for i in data1:
        k.append(states[i])
    data1 = pd.DataFrame(k)
    data1.columns = ["State"]
    #data1.set_index([1:10730])
    h = list(range(1,10731))
    h = pd.Series(h)
    data1[1] = h
    data1.set_index([1],inplace=True)
    #data1["s"] = data8.ix[:,"State"]
    #print(data1.ix[:,["2010-07","2010-08","2010-09"]].head(20))
    data2 = data[[col for col in data.columns if '20' in col]]
    data2 = data2.convert_objects(convert_numeric=True)
    l = 0
    p = 3
    for i in range(2000,2017):
        l1 = [str(i)+"-01",str(i)+"-02",str(i)+"-03"]
        l2 = [str(i)+"-04",str(i)+"-05",str(i)+"-06"]
        l3 = [str(i)+"-07",str(i)+"-08",str(i)+"-09"]
        l4 = [str(i)+"-10",str(i)+"-11",str(i)+"-12"]
        data2[str(i)+'q1'] = data2[l1].mean(axis=1)
        data2[str(i)+'q2'] = data2[l2].mean(axis=1)
        if i != 2016:
            data2[str(i)+'q3'] = data2[l3].mean(axis=1)
            data2[str(i)+'q4'] = data2[l4].mean(axis=1)
        else:
            l5 = [str(i)+"-07",str(i)+"-08"]
            data2[str(i)+'q3'] = data2[l5].mean(axis=1)
        
    #print(data.iloc[0]["2000-01"])#,"2000-02","2000-03"])
    data2 = data2[[col for col in data2.columns if 'q' in col]]
    data2["State"] = data1["State"]
    data2["RegionName"] = data["RegionName"]
    data2.set_index(["State","RegionName"],inplace=True)
    return data2
convert_housing_data_to_quarters()


import scipy
import copy as cp
def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    df = get_list_of_university_towns()
    df1 = convert_housing_data_to_quarters()
    
    df1.reset_index(inplace=True)
    
    mask = df1['State'].isin(df['State']) & df1['RegionName'].isin(df['RegionName'])
    
    dfu = pd.DataFrame(df1[mask])
    dfnu = pd.DataFrame(df1[~mask])
    
    dfnu = dfnu.convert_objects(convert_numeric=True)
    dfu = dfu.convert_objects(convert_numeric=True)
    
    rec_start = get_recession_start()
    rec_bot = get_recession_bottom()
    
    dfnu["PriceRatio1"] = dfnu["2008q2"].div(dfnu[rec_bot])
    dfu["PriceRatio2"] = dfu["2008q2"].div(dfu[rec_bot])
    
    dfnu.reset_index(inplace=True)
    dfu.reset_index(inplace=True)
    
    #dfu.set_index(dfnu.index,inplace=True)
        
    dfun = pd.DataFrame()
    dfun = dfun.convert_objects(convert_numeric=True)
    
    dfun["2008q2nu"] = dfnu["2008q2"]
    dfun["2009q2nu"] = dfnu["2009q2"]
    
    dfun["PriceRatioNU"] = cp.copy(dfnu["PriceRatio1"])
    dfun = dfun.convert_objects(convert_numeric=True)
    
    dfun["2008q2u"] = dfu["2008q2"]
    dfun["2009q2u"] = dfu["2009q2"]
    
    dfun["PriceRatioU"] = dfu["PriceRatio2"]
    
    dfun = dfun.convert_objects(convert_numeric=True)
    
    #print(dfu[dfu.columns == ["2008q2",rec_bot,"PriceRatio"]])
    #print(dfun[["2008q2nu","2009q2nu","PriceRatioNU","2008q2u","2009q2u","PriceRatioU"]])
    
    dfun = dfun.dropna()
    
    t_test = scipy.stats.ttest_ind(dfun["PriceRatioNU"], dfun["PriceRatioU"])
    
    
    p = t_test.pvalue
    if p<0.01:
        different = True
    else:
        different = False
    better = "university town"
    #better = "non-university town"
    final  = (different,p,better)
    return final
run_ttest()


# In[ ]:



