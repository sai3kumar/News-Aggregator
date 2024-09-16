import requests
url = 'https://edition.cnn.com/world'
from bs4 import BeautifulSoup
response = requests.get(url)
response = response.content
categories =['politics','travel','health','entertainment','style','science','climate','sports','world','weather']
info = []
dset =[]
for cat in categories:
  url = 'https://edition.cnn.com/'+cat
  print(url)

  response = requests.get(url)
  response = response.content
  soup = BeautifulSoup(response,'html.parser')
  divs = soup.find_all('div', {'data-component-name': 'card'})

  # Extract href links from anchor tags inside those divs
  data = ['https://edition.cnn.com'+a['href'] for div in divs for a in div.find_all('a', href=True)]

  #don't include already scrapped page
  data = [[i] for i in set(data) if ('comhttp' not in i) ]
  import re
  from datetime import datetime

  #get headline
  for i in data:
      link = i[0]
      res = requests.get(link)
      s = BeautifulSoup(res.content, 'html.parser')
      headline = s.find('h1', {'data-editable': 'headlineText'})
      #print(link)
      #Don't include pages like advertisements
      if(headline == None):
        continue
      i.append(headline.text.strip())
      i.append('CNN')
      date_pattern = r'/(\d{4})/(\d{2})/(\d{2})/'
      match = re.search(date_pattern, link)

      if match:
          year, month, day = match.groups()
          extracted_date = f"{year}-{month}-{day}"
          i.append(extracted_date)
      else:
          datetext = s.find('div',{'class':'timestamp vossi-timestamp-primary-core-light'})
          # Regular expression to match the date (Month Day, Year)
          date_pattern = r'(\w+)\s(\d{1,2}),\s(\d{4})'
          match = re.search(date_pattern, datetext.text)

          if match:
              month_name, day, year = match.groups()

              # Convert the month name to a number (e.g., "September" -> "09")
              month_number = datetime.strptime(month_name, "%B").month

              # Format the date as YYYY-MM-DD
              extracted_date = f"{year}-{month_number:02d}-{int(day):02d}"
              i.append(extracted_date)
          else:
              print("No date found")
              #print(i)
      des = s.find('p',{'data-component-name':'paragraph'})
      try:
        i.append(des.text.strip())
      except:
        #if the page has got only headline
        i.append(headline.text.strip())
  for i in data:
    i.append(cat)
  info.extend(data)
  print(len(data))
print(len(info))
print(info[0])
import pandas as pd
df = pd.DataFrame(info,columns=['link','headline','source','date','description','category'])
df.to_csv('news_articles.csv', index=False)