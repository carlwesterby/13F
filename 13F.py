import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import glob
import os.path
import html5lib
from bs4 import BeautifulSoup
import bs4 as bs
import requests
import requests_random_user_agent
import edgar
import time
import datetime
from datetime import datetime
download_directory=r'C:\Users\YOUR_DIRECTORY_HERE'
since_year=1993
landing_pages=[]
#loop through each file and pull out the landing pages
for file in files:
    #read the current file
    temp_DF = pd.read_csv(download_directory+'/'+file, delimiter="|")
    #set the columns of interest
    columns=["CIK", "Name", "Report", "Date", "Txt_URL","HTML_URL" ]
    temp_DF.columns =columns
    #filter the company that we want
    temp_DF=temp_DF[temp_DF['Name']=='BERKSHIRE HATHAWAY INC']
    #grab the filing that we want
    temp_DF=temp_DF[temp_DF['Report']=='13F-HR']
    #grab the url of the landing page
    temp=temp_DF['HTML_URL'].values
    #append it if it exists
    if(len(temp)!=0):
        landing_pages.append(temp[0])
URL_start='https://www.sec.gov/Archives/'
main_pages=[]
file_list_2=[]
#go to each landing page
for page in landing_pages:
    #delay to avoid hitting the SEC rate limit
    time.sleep(1)
    URL=URL_start+page
    #grab the page
    page=requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    #for each link in the landing page
    for link in soup.table.find_all('a'):
        #if the link contains html and has "Table" then the link has the stock table
        if( ('html' in str(link)) and ('Table' in str(link.get('href'))) ):
            main_pages.append(link)
file_new=files[len(files)-len(main_pages):]
time=[]
for item in file_new:
    time.append(item)#[0:9])
#new base for the actual pages
index='https://www.sec.gov/'
output=r"C:\Users\cwesterb\Stocks\13Foutput"
#loop through each of the pages and grab the stocks
count=0
shares=[]
value=[]
combined_DF=pd.DataFrame()
totalstock_DF=pd.DataFrame()
for item in main_pages:
    time.sleep(1)
    page=requests.get(index+item)
    soup = BeautifulSoup(page.content, 'html.parser')
    print(index+item)
    #grab all the tables
    dsf=pd.read_html(page.content)
    current_len=0
    #find the longest
    for entry in dsf:
        print(len(entry))
        if(len(entry)>current_len):
            current_len=len(entry)
            company_table=entry
    #format columns
    company_table.columns = company_table.iloc[2]
    company_table=company_table.iloc[3:]
    #grab company name, total value, and number of shares
    company_table=company_table[['NAME OF ISSUER','(x$1000)','PRN AMT']]
    #force the value and stocks to be numbers
    cols=['(x$1000)', 'PRN AMT']
    company_table[cols] = company_table[cols].apply(pd.to_numeric, errors='coerce', axis=1)
    #combine duplicate company name entries by summing the value and # of shares
    DF=company_table.groupby(['NAME OF ISSUER']).sum()
    df1 = pd.DataFrame(DF['(x$1000)']).transpose()
    df1.index=[file_new[count]]
    combined_DF=combined_DF.append(df1)
    #redo for the number of shares
    df1 = pd.DataFrame(DF['PRN AMT']).transpose()
    df1.index=[file_new[count]]
    totalstock_DF=totalstock_DF.append(df1)
    count=count+1
#fill empties with 0's and push data to .csv files
combined_DF=combined_DF.fillna(0)
totalstock_DF=totalstock_DF.fillna(0)
combined_DF.to_csv(r"C:\Users\YOUR_NAME\13Foutput"+'/Berkshire_Hathaway_holdings.csv')
totalstock_DF.to_csv(r"C:\Users\YOUR_NAME\13Foutput"+'/Berkshire_Hathaway_shares.csv')
