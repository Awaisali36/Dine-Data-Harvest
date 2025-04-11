from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import time
import streamlit as st
import json
import matplotlib.pyplot as plt

def getRating(url):

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    time.sleep(2)
    
    Dates = []
    Ratings = []
    
    page = 0
    driver.get(url)
    time.sleep(2)
    
    while True:
        if (page == 20):
            break
        try:
            Data1 = BeautifulSoup(driver.page_source, 'html.parser')
            Data2 = Data1.find_all('div', class_='MpiILQAMSSg-')
            
            for D in Data2:
                try:
                    date = D.find('p', class_='iLkEeQbexGs-')
                    if date:
                        date = str (date.text)[9:]  
                        date = datetime.strptime(date, "%B %d, %Y").date()
                        Dates.append(str(date))
                    
                    rating = D.find('span', class_='-y00OllFiMo-')
                    if rating:
                        Ratings.append(str (rating.text))
                except :
                    continue
            
            print(f"Scraped {len(Dates)} reviews so far.")

            try:
                next = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[aria-label="Go to the next page"]')))
                next.click()
                page+=1
                time.sleep(2)  
            except TimeoutException:
                break
        
        except StaleElementReferenceException:
            print("A stale element encountered .. . . ")
            continue
        except Exception as e:
            print(f"Error: {e}")
            break
    
    driver.quit()
    
    return pd.DataFrame({'Date': Dates, 'Rating': Ratings})

def getRestaurantName(url):
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    time.sleep(2)
    driver.get(url)
    time.sleep(2)
    name = ''
    
    
    Data1 = BeautifulSoup(driver.page_source, 'html.parser')
    Data2 = Data1.find('h1', class_='E-vwXONV9nc-')
    Data3 = Data1.find_all ('span', class_ = 'yEg-cOaKGpI-') 

    name = str(Data2.text)
    r1 = str (Data3[0].text)
    r2 = str (Data3[1].text)
    r3 = str (Data3[2].text)
    r4 = str (Data3[3].text)
    print (r1)
    print (r2)
    print (r3)
    print (r4)
    driver.quit()
    return pd.DataFrame({'Restaurant_Name': [name],
                  'Food_Rating': [r1],
                  'Service_Rating': [r2],
                  'Ambience_Rating': [r3],
                  'Value_Rating': [r4]
                  })

def Title():
    st.markdown(
        """
        <div style="background-color:#982608; padding:10px; border-radius:8px;">
            <h1 style="color:white; text-align:center;">Competitor Analysis</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

def Title2():
    st.markdown(
        """
        <div style="background-color:#982608; padding:10px; border-radius:8px;">
            <h1 style="color:white; text-align:center;">Overall Comparison</h1>
        </div>
        """,
        unsafe_allow_html=True,
    )
def inputURL () :
    st.markdown(
        """
        <style>
            
            button {
                background-color: #982608;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background-color: #c44900;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    url = st.text_input("URL", placeholder="Enter the restaurant URL")

    if st.button("OK"):
        Data = getRating(url)
        Data.to_csv('OtherRatting.csv', index= False)
        d = getRestaurantName(url)
        d.to_csv ('other_restaurant_name.csv', index = False)

def barPlot (list1 , list2, name1, name2):
    x = ['Food','Service','Ambience','Value']
    fig, ax = plt.subplots()

    ax.bar(x, list1, width=0.4, label=name1, align='center', color='#802004', alpha=0.7)
    ax.bar(x, list2, width=0.4, label=name2, align='edge', color='#044330', alpha=0.7)

    ax.set_xlabel('Rating')
    ax.set_ylabel('Value')
    ax.set_title('Overall Comparison of Restaurants')

    ax.legend()

    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)

def plotGraph(data1 , data2, name1 , name2):
   
    fig, ax = plt.subplots()
    ax.plot(data1["Date"], data1["Rating"], label= name1, color="#802004")
    ax.plot(data2["Date"], data2["Rating"], label=name2 , color="#044330")

    ax.set_title("Time Series of Reviews")
    ax.set_xlabel("Date")
    ax.set_ylabel("Rating")
    ax.legend()
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)

def showPlot():
    st.markdown(
        """
        <style>
            
            button {
                background-color: #982608;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background-color: #c44900;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Show Time Series"):
        try:
            data1 = pd.read_csv('ratings.csv')
            data2 = pd.read_csv('OtherRatting.csv')
            data3 = pd.read_csv('restaurant_name.csv')
            myRestName = data3['Restaurant_Name'][0]
            data4 = pd.read_csv('other_restaurant_name.csv')
            restName = data4['Restaurant_Name'][0]

            List1 = []
            List1.append (data3['Food_Rating'][0])
            List1.append (data3['Service_Rating'][0])
            List1.append (data3['Ambience_Rating'][0])
            List1.append (data3['Value_Rating'][0])

            List2 = []
            List2.append (data4['Food_Rating'][0])
            List2.append (data4['Service_Rating'][0])
            List2.append (data4['Ambience_Rating'][0])
            List2.append (data4['Value_Rating'][0])


            temp_data1 = data1[data1['Date'].isin(data2['Date'])]
            temp_data2 = data2[data2['Date'].isin(data1['Date'])]
            for i in range(0, min(len(temp_data1), len(temp_data2)), 20):
                temp1 = temp_data1.iloc[i:i+20]
                minDate = temp1['Date'].min()
                maxDate = temp1['Date'].max()
                try :

                    t1 = temp_data1[(temp_data1['Date'] >= minDate) & (temp_data1['Date'] <= maxDate)]
                    t2 = temp_data2[(temp_data2['Date'] >= minDate) & (temp_data2['Date'] <= maxDate)]
                    plotGraph(t1, t2, myRestName, restName)
                except:
                    st.markdown(
                        """
                        <div style="background-color:red; padding:10px; border-radius:8px;">
                            <h3 style="color:white; text-align:center;">Error.</h3>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    continue
            Title2()
            barPlot(List1, List2, myRestName, restName)
        except:
            st.markdown(
                """
                <div style="background-color:red; padding:10px; border-radius:8px;">
                    <h3 style="color:white; text-align:center;">Error: File not found.</h3>
                </div>
                """,
                unsafe_allow_html=True,
            )

Title()
inputURL()
showPlot()