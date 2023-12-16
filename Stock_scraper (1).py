#!/usr/bin/env python
# coding: utf-8

# #   MARKET MINDS INSIGHTS HUB

# ### Importing Packages

# In[1]:


from bs4 import BeautifulSoup 
import requests
import pandas as pd
import datetime
import re
from matplotlib import pyplot as plt


# ### Creating dictionary to store scraped values

# In[2]:


stock ={"S.No":[],"Names":[],"Current Market Price Rs":[],"Price to Earning Rs.Cr":[],"Market Capitalization":[],
        "Dividend Yield %":[],"Net Profit Latest Quarter Rs.Cr":[],"Quarterly Profit Growth":[],"Sales Latest Quater Rs.Cr":[],
        "Quarterly Sales Growth%":[],"Return On Capital Employed%":[]}


# In[3]:


stock_list = []
def scraper(soup_obj):
    for data in soup_obj:
        stock_list.append(data.get_text(strip=True))


# ### Creating a loop to iterate the scraping process and get data from all the pages of the website

# In[4]:


for page in range(1,12): 
    url = f"https://www.screener.in/screens/885655/top-100-stocks/?page={page}"
    req = requests.get(url)
    soup =  BeautifulSoup(req.content,"html.parser")
    soup = soup.find_all("td")
    scraper(soup)


# In[5]:


column = list(stock.keys())


# In[6]:


column


# In[7]:


stock_list[0:11]


# ### Inserting the scraped data to dictionary

# In[8]:


index = 0
for i in stock_list:
    if index > 10:
        index = 0
    stock[column[index]].append(i)
    index+=1     


# ### Creating a pandas data frame for data cleaning and analysis

# In[9]:


stock_data = pd.DataFrame(stock)


# In[10]:


stock_data[0:30]


# In[11]:


stock_data = stock_data.drop_duplicates()


# ### removing the value named median 

# In[12]:


pattern="Median.*"
for i in stock_data["Names"]:
    if re.match(pattern,i):
        index=stock_data.loc[stock_data["Names"]==i].index
        stock_data=stock_data.drop(index)


# In[13]:


stock_data.info()


# ### Converting the data to their respective data types

# In[14]:


data_type = stock_data.keys()[2:]
data_type


# In[15]:


for i in data_type:
    new_list = []
    for j in stock_data[i]:
        try:
            new_list.append(float(j))
        except:
            new_list.append(0)
    stock_data[i] = new_list
    


# In[16]:


stock_data.info()


# ### creating a date and time column to analyze trend

# In[17]:


stock_data["Date"] = datetime.date.today()
stock_data["Time"] = datetime.datetime.now().time()


# In[18]:


stock_data.describe()


# In[19]:


stock_data.head()


# ### Inserting the cleaned data to MySQL database for further analysis

# In[20]:


from sqlalchemy import create_engine,text
import mysql.connector


# In[21]:


url = 'mysql+mysqlconnector://root:****@localhost/top_stocks'
engine = create_engine(url)


# In[22]:


table_name = "stocks_table"
stock_data.to_sql(name=table_name, con=engine, if_exists='append', index=False)


# ### Performing EDA 

# In[23]:


stock_data = stock_data.sort_values("Current Market Price Rs",ascending=False)
plt.figure(figsize=(28,12))
plt.title("TOP STOCKS BY CURRENT MARKET PRICE",fontsize=20,fontweight='bold')
plt.bar(stock_data["Names"][0:10],stock_data["Current Market Price Rs"][0:10],color='green')
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.show()


# In[24]:


stock_data = stock_data.sort_values("Net Profit Latest Quarter Rs.Cr",ascending=False)
plt.figure(figsize=(20,7))
plt.title("TOP STOCKS BY NET PROFIT LATEST QUARTER",fontsize=20,fontweight='bold')
plt.barh(stock_data["Names"][0:10],stock_data["Net Profit Latest Quarter Rs.Cr"][0:10],color="purple")
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.show()


# In[25]:


stock_data = stock_data.sort_values("Market Capitalization",ascending=False)
plt.figure(figsize=(28,10))
c = ['red', 'blue', 'green', 'purple', 'orange', 'cyan', 'magenta', 'yellow', 'brown', 'gray']
plt.title("TOP STOCKS BY MARKET CAPITALIZATION",fontsize=20,fontweight='bold')
plt.bar(stock_data["Names"][0:10],stock_data["Market Capitalization"][0:10],color=c)
plt.xticks(fontsize=17,fontweight='bold')
plt.yticks(fontsize=16)
plt.show()


# In[26]:


plt.figure(figsize=(20,7))
stock_data =stock_data.sort_values("Quarterly Profit Growth",ascending=False)
plt.pie(stock_data["Quarterly Profit Growth"][0:10],labels=stock_data["Names"][0:10],autopct="%0.1f%%")
plt.title("TOP STOCKS BY QUARTERLY PROFIT GROWTH %",fontsize=15,fontweight="bold")
plt.legend(bbox_to_anchor=(1.2, 0.5), loc="center left")
plt.show()


# In[27]:


plt.figure(figsize=(25,10))
stock_data =stock_data.sort_values("Current Market Price Rs",ascending=False)
plt.bar(stock_data["Names"][0:10],stock_data["Sales Latest Quater Rs.Cr"][0:10],label="Sales Latest Quarter in crores",color="darkgreen")
plt.bar(stock_data["Names"][0:10],stock_data["Net Profit Latest Quarter Rs.Cr"][0:10],label="Net profit Latest Quarter in Crores",color="darkred")
plt.title("TOP STOCKS BY CURRENT MARKET PRICE",fontsize=20,fontweight='bold')
plt.xticks(fontsize=16)
plt.yticks(fontsize=18)
plt.legend(fontsize=20)
plt.show()


# In[28]:


plt.figure(figsize=(25,10))
stock_data =stock_data.sort_values("Return On Capital Employed%",ascending=False)
w=0.6
plt.bar(stock_data["Names"][0:10],stock_data["Return On Capital Employed%"][0:10],w,label="Return On Capital Employed%",color="green")
plt.bar(stock_data["Names"][0:10],stock_data["Quarterly Profit Growth"][0:10],w,label="Quarterly Profit Growth",color="red")
plt.title("TOP STOCKS BY CURRENT MARKET PRICE",fontsize=20,fontweight='bold')
plt.xticks(fontsize=16)
plt.yticks(fontsize=18)
plt.legend(fontsize=20)
plt.show()


# In[29]:


with engine.connect() as connection:
    query = text('SELECT * FROM stocks_table')
    execution = connection.execute(query)
    table = execution.fetchall()
table[0:10]
    


# In[30]:


table = pd.DataFrame(table)
table


# In[31]:


value =table[table["Names"]=="TCS"]
plt.figure(figsize=(20,7))
plt.plot(value["Date"],value["Current Market Price Rs"],color='red',linewidth=5,label="Current Market Price Rs")
plt.legend(fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.title("TCS - CURRENT MARKET PRTCE TREND ON DAYS",fontweight='bold',fontsize=20)
plt.show()


# In[32]:


value =table[table["Names"]=="Reliance Industr"]


# In[33]:


value = table[table["Names"]=="Infosys"]


# In[34]:


plt.figure(figsize=(20,7))
plt.plot(value["Date"],value["Dividend Yield %"],color='darkgreen',linewidth=5,label="Dividend Yeild %")
plt.legend(fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.title("INFOSYS - DIVIDEND TREND",fontweight='bold',fontsize=25)
plt.show()


# In[35]:


plt.figure(figsize=(20,7))
plt.plot(value["Date"],value["Quarterly Profit Growth"],color='red',linewidth=5,label="Quarterly Profit Growth")
plt.plot(value["Date"],value["Quarterly Sales Growth%"],color='green',linewidth=5,label="Quarterly Sales Growth%")
plt.plot(value["Date"],value["Return On Capital Employed%"],color='blue',linewidth=5,label="Return On Capital Employed%")
plt.plot(value["Date"],value["Current Market Price Rs"],color='purple',linewidth=5,label="Current Market Price Rs")
plt.legend(fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.title("RELIANCE INDUSTRY TREND",fontweight='bold',fontsize=25)
plt.show()


# In[36]:


value = table[table["Names"]=="Adani Power"]
plt.figure(figsize=(20,7))
plt.plot(value["Date"],value["Quarterly Profit Growth"],color='red',linewidth=5,label="Quarterly Profit Growth%")
plt.plot(value["Date"],value["Quarterly Sales Growth%"],color='green',linewidth=5,label="Quarterly Sales Growth%")
plt.plot(value["Date"],value["Return On Capital Employed%"],color='blue',linewidth=5,label="Return On Capital Employed%")
plt.plot(value["Date"],value["Current Market Price Rs"],color='purple',linewidth=5,label="Current Market Price Rs")
plt.legend(fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.title("ADANI POWER TREND",fontweight='bold',fontsize=25)
plt.show()


# In[37]:


value = table[table["Names"]=="Adani Ports"]
plt.figure(figsize=(20,7))
plt.plot(value["Date"],value["Quarterly Profit Growth"],color='red',linewidth=5,label="Quarterly Profit Growth%")
plt.plot(value["Date"],value["Quarterly Sales Growth%"],color='green',linewidth=5,label="Quarterly Sales Growth%")
plt.plot(value["Date"],value["Return On Capital Employed%"],color='blue',linewidth=5,label="Return On Capital Employed%")
plt.plot(value["Date"],value["Current Market Price Rs"],color='purple',linewidth=5,label="Current Market Price Rs")
plt.legend(fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.title("ADANI PORTS TREND",fontweight='bold',fontsize=25)
plt.show()


# In[38]:


value = table[table["Names"]=="Adani Total Gas"]
plt.figure(figsize=(20,7))
plt.plot(value["Date"],value["Quarterly Profit Growth"],color='red',linewidth=5,label="Quarterly Profit Growth%")
plt.plot(value["Date"],value["Quarterly Sales Growth%"],color='green',linewidth=5,label="Quarterly Sales Growth%")
plt.plot(value["Date"],value["Return On Capital Employed%"],color='blue',linewidth=5,label="Return On Capital Employed%")
plt.plot(value["Date"],value["Current Market Price Rs"],color='purple',linewidth=5,label="Current Market Price Rs")
plt.legend(fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.title("ADANI TOTAL GAS TREND",fontweight='bold',fontsize=25)
plt.show()


# In[39]:


value = stock_data[stock_data["Quarterly Profit Growth"]<0]
value = value.sort_values("Quarterly Profit Growth")
plt.figure(figsize=(30,10))
plt.bar(value["Names"][0:10],value["Quarterly Profit Growth"][0:10],color='darkred',label="Quarterly Profit Growth %")
plt.legend(fontsize=20)
plt.xticks(fontsize=18)
plt.yticks(fontsize=18)
plt.title("COMPANIES IN LOSS",fontweight='bold',fontsize=35)
plt.show()


# In[40]:


value=stock_data
value = value.sort_values("Return On Capital Employed%",ascending=False)
plt.figure(figsize=(30,15))
plt.barh(value["Names"][0:15],value["Return On Capital Employed%"][0:15],color='crimson',label="Return On Capital Employed%")
plt.barh(value["Names"][0:15],value["Quarterly Profit Growth"][0:15],color='blue',label="Quarterly Profit Growth %")
plt.legend(fontsize=20)
plt.xticks(fontsize=18)
plt.yticks(fontsize=25)
plt.title("RETURN ON CAPITAL EMPLOYED AND QUARTERTLY PROFIT GROWTH",fontweight='bold',fontsize=35)
plt.show()


# In[41]:


value=stock_data.sort_values("Quarterly Sales Growth%",ascending=False)
plt.figure(figsize=(30,15))
plt.barh(value["Names"][0:15],value["Quarterly Sales Growth%"][0:15],color='crimson',label="Quarterly Sales Growth%")
plt.barh(value["Names"][0:15],value["Quarterly Profit Growth"][0:15],color='darkolivegreen',label="Quarterly Profit Growth %")
plt.legend(fontsize=20)
plt.xticks(fontsize=18)
plt.yticks(fontsize=25)
plt.title("QUARTERTLY PROFIT GROWTH AND QUARTERLY SALES GROWTH",fontweight='bold',fontsize=35)
plt.show()


# In[42]:


plt.figure(figsize=(20,7))
stock_data =stock_data.sort_values("Dividend Yield %",ascending=False)
plt.pie(stock_data["Dividend Yield %"][0:10],labels=stock_data["Names"][0:10],autopct="%0.1f%%")
plt.title("TOP STOCKS BY DIVIDEND YEILD %",fontsize=15,fontweight="bold")
plt.xticks(fontsize=20)
plt.legend(bbox_to_anchor=(1.2, 0.5), loc="center left")
plt.show()

