import pandas as pd
import urllib
import requests
from bs4 import BeautifulSoup
import time
       
dataset=pd.DataFrame(columns=['Image',"Name"])

j=0
url='https://en.wikipedia.org/wiki/List_of_Indian_film_actors'

response = requests.get(url, proxies=urllib.request.getproxies())
soup = BeautifulSoup(response.text, "html.parser")

name_box = soup.find_all('div', attrs={'class': 'div-col columns column-width'})
      
        
 
def wiki(j,url):    
    
    response = requests.get(url, proxies=urllib.request.getproxies())
    soup = BeautifulSoup(response.text, "html.parser")
    
    
    
    table = soup.find('table', attrs={'class': 'infobox biography vcard'})
    if table:
        rows = table.find_all('tr')
    else :
        return j

    j=j+1
    for i,row in enumerate(rows):
        time.sleep(1)
        
        if i==0:
           cells2 = row.find('th')
           dataset.loc[j,'Name']=cells2.text
           
          # print(cells.text)
           print(cells2.text)    
           
        elif row.find('img'):
            img=row.find('img')['src']
            dataset.loc[j,'Image']='https:'+img
            
            print(img)
        elif row.find('th') and row.find('td'):
            
            if row.find('sup'):
             row.find('sup').decompose()
            if row.find('span'):
             row.find('span').decompose()
            cells2 = row.find('th')
            cells = row.find('td')
            dataset.loc[j,cells2.text]=cells.text
            
            print(cells.text)
            print(cells2.text) 
    return j 
           
       
for row in name_box:
    names = row.find_all('a')
    time.sleep(1)
    for name in names:
        print (name['href'])
        url='https://en.wikipedia.org'+name['href']
        j=wiki(j,url)       
       
       
#second website       
       

url='http://www.leoranews.com/category/profiles/bollywood-actress-profile/'

def actor_profiles(url):
    time.sleep(1)
    
    response = requests.get(url, proxies=urllib.request.getproxies())
    soup = BeautifulSoup(response.text, "html.parser")
    
    actor_profile = soup.find_all('h2', attrs={'class': 'entry-title'})
    return actor_profile

def get_data(url,tag,class_type):
    time.sleep(1)
    response = requests.get(url, proxies=urllib.request.getproxies())
    soup = BeautifulSoup(response.text, "html.parser")
    
    data = soup.find(tag, attrs={'class': class_type})
    
    return data

def call(actor_profile,j):
    for i,profile in enumerate(actor_profile):
        
        profile_link = profile.a['href'] 
        
        table=get_data(profile_link,'table','MsoNormalTable aligncenter')
        
            
        rows = table.find_all('tr')
        col1=[]
        col2=[]
        for row in rows:
            cells = row.find_all('td')
            if len(cells)==2:
                
                dataset.loc[j,cells[0].text.strip()]=cells[1].text.strip()
                
                
          
        img_data=get_data(profile_link,'img','attachment-glob-medium size-glob-medium wp-post-image')
        time.sleep(1)    
        img=img_data['src']
        time.sleep(1)
        dataset.loc[j,'Image']=img
        j=j+1  
        
        print('img',img)
    return j

for i in range(13):
    
    actor_profile=actor_profiles(url)
    j=call(actor_profile,j)
    url='http://www.leoranews.com/category/profiles/bollywood-actress-profile/page/'
    url=url+str(i+2)+'/'
    print('next page')
      
       
       
       
       
       
       
       
       
       
       

