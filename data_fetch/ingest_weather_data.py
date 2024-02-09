# Project 2 -  Data Ingestion Container  
# Fetch Weather data via API call

from bs4 import BeautifulSoup
import requests
import pandas as pd
import pymongo 
import json
import time

print('Ingest Weather data')

def scrape_single_city_page(soup, city_list):
  """
  Function to Scrap a single page
  Scrape the city page content given by Soup object <soup>
  The found cities are stored in the list <city_list>
  """

  print('Scrap Single City page')

  # Get City table:
  city_tab = soup.find('table', class_='table table-hover table-bordered')

  for row in city_tab.find_all('tr'):
    cols = row.find_all('td')

    if cols:
      # Structure of City table:
      # [0] City number
      # [1] City name
      # [2] Country
      # [3] Latitude
      # [4] Longitude

      city_list.append(
            {
                'city_number': cols[0].text.strip(),
                'city_name': cols[1].text.strip(),
                'country': cols[2].text.strip(),
                'latitude': float(cols[3].text.strip()),
                'longitude': float(cols[4].text.strip())
            })

# Function: Get Next Page within City Main URL
def get_next_page(soup, main_url):
  """
  Function to get the next page for the URL <main_url>
  Return : The URL for the next page
  """
  print('Search for next page')

  next_page_url = None
  next_page_link = soup.find_all('a', class_='page-link')
  for link in next_page_link:
    if link.text == "Next":
      print('Next page:')
      print(link['href'])
      # Get next page for main URL
      if link['href'].startswith(main_url) :
        next_page_url = link['href']
  return next_page_url

# Function Scrape all pages for the City Main URL
def scrape_all_city_data(main_url):
  '''
  Scrap all city pages for the URL <main_url>

  Return: Dataframe <df> which contains the City data
  '''
  print('Scrap all City pages')
  html_req = requests.get(main_url)
  soup = BeautifulSoup(html_req.text, 'html.parser')

  # Main list objects which collects the City metadata
  city_list = []

  # Scrap the first page
  scrape_single_city_page(soup, city_list)

  # Check if a next page is available
  next_page_url = get_next_page(soup, main_url)

  # Traverse through the next pages to collect
  # the data for all cities
  while next_page_url is not None:

    # Take the next page, scrap it and (if available) search for the (overnext) page
    html_req = requests.get(next_page_url)
    soup = BeautifulSoup(html_req.text, 'html.parser')
    scrape_single_city_page(soup, city_list)
    next_page_url = get_next_page(soup, main_url)

  # Store the results in a DataFrame
  df = pd.DataFrame(city_list)

  return df

def get_weather_data(latitude, longitude, appid):
  '''
   Extract the Weather data for the coordinates
   and return a JSON Object
   '''
  weather_data = dict()
  # Define the URL
  # Uncomment this line and please use this carefully: the appid is limited to 1,000,000 calls/month and 60 calls/minute
  url = f"https://api.openweathermap.org/data/2.5/weather?lat={str(latitude)}&lon={str(longitude)}&units=metric&appid={appid}"

  # Make the request and get the response object
  response = requests.get(url)

  # Check if the request was successful
  if response.status_code == 200:
    # Parse the JSON content from the response
    data = response.json()
    #print(data)
  else:
    print(f"Failed to retrieve data, status code: {response.status_code}")
    return weather_data

  #weather_data['temperature'] = data['main']['temp']
  #weather_data['weather'] = data['weather'][0]['main']
  #weather_data['weather_description'] = data['weather'][0]['description']
  weather_data = data 

  return weather_data

def main():
   # Main program
   # Overall parameters - needed for API Call
   # OpenWeather API:
   #openweather_appid = 'e88b8a7f2403142335eb142bbbdceed5'  # Laszlos
   openweather_appid = '19f9b7de91755a5dc972bc7e1e09f6b7'   # Juergen

   # City URLs
   # Germany
   main_url="https://geokeo.com/database/city/de"
   # Hungary
   #main_url="https://geokeo.com/database/region/hu/"

   print('Start main program')
   print(f"Scrap {main_url}")

   # Caution: geokeo.com is sometimes not available !


   html_req = requests.get(main_url)
   soup = BeautifulSoup(html_req.text, 'html.parser')

   # Scrape the City data for main URL
   df = None
   df = scrape_all_city_data(main_url)

   # Reduce to 10 cities
   df = df.head(10)

   # Calculate the Weather Data for the Cities
   # The function provides a JSON object 
   # Value for additional (3.) Call parameter (appid) is set beforehand in Main script

   print('Get Weather data')
   df['weather_data'] = df.apply(lambda row, appid=openweather_appid: get_weather_data(row['latitude'], row['longitude'], appid), axis=1)

   print('Extracted Weather data')
   print(df)

   # Convert JSON Objects into list
   print('Convert Weather Data JSON Object into a MongoDB-readable format')
   json_weather_data = df['weather_data'].to_list()


   # Hard coded example, because geokeo is currently (sometimes) not available
   '''
   ccity_number          city_name  country   latitude  longitude
              1             Aachen  Germany  50.776351   6.083862
              2           Augsburg  Germany  48.366804  10.898697
              3  Bergisch Gladbach  Germany  50.992930   7.127738
              4             Berlin  Germany  52.517036  13.388860
              5             Berlin  Germany  52.517036  13.388860
              6          Bielefeld  Germany  52.019100   8.531007
              7             Bochum  Germany  51.481811   7.219664
              8               Bonn  Germany  50.735851   7.100660
              9            Bottrop  Germany  51.521581   6.929204
             10             Bremen  Germany  53.075820   8.807165

   json_weather_data = get_weather_data(52.517036, 13.388860, openweather_appid)

   print(json_weather_data)
   '''

   # Connect to the MongoDB database
   print("Connect to MongoDB")
   client = pymongo.MongoClient("mongodb://mongodb:27017/")

   # Database 
   db = client["data_db"]

   collection = db["data_collection"]

   # For clean-up reason drop the collection
   # collection.drop()

   print('Number of documents already in the collection:', collection.count_documents({}))

   print('Store Weather data in MongoDB Collection')

   if isinstance(json_weather_data, list):
        collection.insert_many(json_weather_data)  
   else:
        collection.insert_one(json_weather_data)

   print('Weather data in MongoDB Collection after insert')
   for doc in collection.find():
       print(doc)    

   print('Number of documents after load in the collection:', collection.count_documents({}))

   print('End main program')


#################################################################################
# Call Main program

# Scheduling of Main program:
# Can be limited by: number of interations : <max_interations>
# 0 : No limit

# Setting time delay after each execution:
# Number of seconds to wait for the next execution: <sleeping_time_sec>

max_interations=5

# Sleeping for 30 Minutes
sleeping_time_sec=60*30

if max_interations == 0:
  print('Unlimited iterations')
else:
  print('Iterations limited to:', max_interations)

iteration_flag=True
loop_cnt = 1
while iteration_flag:
  print('Loop-Cnt:', loop_cnt)  
  
  main()
  
  loop_cnt = loop_cnt + 1

  if loop_cnt > max_interations and max_interations != 0:
    # Maximum iterations reached 
    print('Maximum iterations reached - stop processing')
    iteration_flag = False

  if iteration_flag == True: 
    print('Sleep for: ', sleeping_time_sec, 'seconds')  
    time.sleep(sleeping_time_sec)

