# -*- coding: utf-8 -*-
"""
#author : Ranjith James

# This code is meant to Scrape Reddit and Post question from Reddit to Quora In order,
to automate the process of asking questions for the Quora Partner Program
"""

from   selenium import webdriver
from   selenium.common.exceptions import TimeoutException
import requests
import csv
import time
from bs4 import BeautifulSoup
import pandas as pd
from pynput.keyboard import Key, Controller
keyboard = Controller()
import win32api, win32con
import os
from selenium.webdriver.support.ui import Select

# if file does not exist write header 
cout=1
time.sleep(1)
for i in range(0,4  ):
    
    url = "https://old.reddit.com/r/AskReddit/new/"
    # Headers to mimic a browser visit 
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    # Returns a requests.models.Response object
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    
    domains = soup.find_all("span", class_="domain")
    
    for domain in domains:
        print(domain.text)
        parent_div = domain.parent
        print(parent_div.text)
        
    attrs = {'class': 'thing', 'data-domain': 'self.AskReddit'}
    df = pd.DataFrame(columns=['QUES', 'ASKED',"Answer"])
        
    counter = 1
    while (counter <=400):
        for post in soup.find_all('div', attrs=attrs):
            title = post.find('p', class_="title").text
            post_line = [title]
#            ur=post.find('a', href=True)['href']
#            url = "https://www.reddit.com"+ur
#            xyz = requests.get(url, headers=headers)
#            xyz1 = BeautifulSoup(xyz.text, 'html.parser')
#            comm = xyz1.find(attrs={"data-test-id": "comment"})
            try:
#                comm=comm.text
                row=[post_line,"NO",""]
            except:
                row=[post_line,"NO",""]    
            df.loc[len(df)] = row
    #        with open(r'E:\DA\output.csv', 'a') as f:
    #            writer = csv.writer(f)
    #            writer.writerow(post_line)
        
            counter += 1    
        next_button = soup.find("span", class_="next-button")
        next_page_link = next_button.find("a").attrs['href']
        time.sleep(2)
        page = requests.get(next_page_link, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
    
    ques=df
    ques['QUES']=ques['QUES'].astype(str)
    #ques=pd.read_csv(r'E:\DA\output.csv',encoding = "ISO-8859-1")
    
    ques.iloc[:,0] = ques.iloc[:,0].str.replace('(self.AskReddit)','')
    
    ques.iloc[:,0] = ques.iloc[:,0].str.replace('[','')
    ques.iloc[:,0] = ques.iloc[:,0].str.replace(']','')
    
    ques.iloc[:,0] = ques.iloc[:,0].str.replace('serious','')
    
    
    
    ques.iloc[:,0] = ques.iloc[:,0].str.replace('Serious Replies Only','')
    
    ques.iloc[:,0] = ques.iloc[:,0].str.replace('Serious ','')
    
    ques.iloc[:,0]=ques['QUES'].str.replace(r"[\"\',]", '')
     
     
    
    
    ques.iloc[:,0] = ques.iloc[:,0].str.replace('(','')
    ques.iloc[:,0] = ques.iloc[:,0].str.replace(')','')
    ques.iloc[:,0] = ques.iloc[:,0].str.replace('of Reddit','')
    
    ques.iloc[:,0] = ques.iloc[:,0].str.replace('of reddit','')
    
    ques.iloc[:,0] = ques.iloc[:,0].str.replace('Reddit','')
    ques.iloc[:,0] = ques.iloc[:,0].str.replace('reddit','')
    ques.iloc[:,0] = ques.iloc[:,0].str.replace("'","'")
    ques.iloc[:,0] = ques.iloc[:,0].str.replace("Ors ","Others ")
    ques.iloc[:,0] = ques.iloc[:,0].str.replace("ORS ","Others ")
    ques.iloc[:,0] = ques.iloc[:,0].str.replace("ors ","Others ")
    ques.iloc[:,0] = ques.iloc[:,0].str.replace("Ors,","Others,")
    
    
    ques.iloc[:,0] = ques.iloc[:,0].str.strip()
    
    if not os.path.isfile(r'C:\Users\Ranjith James\Documents\output.csv'):
       ques.to_csv(r"C:\Users\Ranjith James\Documents\output.csv", header='column_names',index=False)
    else: # else it exists so append without writing the header
       ques.to_csv(r'C:\Users\Ranjith James\Documents\output.csv', mode='a', header=False,index=False)
    
    
    ques_old=pd.read_csv(r'C:\Users\Ranjith James\Documents\output.csv')
    
    ques_old.drop("length",axis=1,inplace=True)
    
    ques3=ques_old.append(ques)
    
    ques3=ques3.drop_duplicates(subset=['QUES'])
    
    ques=ques3
                    
    
    def click(x,y):
        win32api.SetCursorPos((x,y))
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)
    browser = webdriver.Chrome(r"C:\Users\Ranjith James\Documents\chromedriver.exe")
    browser.get("http://www.quora.com")
    
    login=browser.find_element_by_css_selector(".text.header_login_text_box.ignore_interaction")
    login.click()
    login.send_keys("ranjithjames1994@gmail.com")
    
    login=browser.find_element_by_css_selector('input[placeholder=Password]')
    login.click()
    
    login.send_keys("*****ENTER YOUR PASSWORD ******")
    time.sleep(5)
    login=browser.find_element_by_css_selector('input[value=Login]')
    login.click()
    
    
    
    browser.maximize_window()
    
    time.sleep(5)
    
    import numpy as np
    ques = ques.replace(np.nan, '', regex=True)
    
    ques=ques[~ques.Answer.str.contains("subreddit")]
    
    ques['length'] = ques['Answer'].str.len()
    ques.sort_values('length', ascending=False, inplace=True)
    
    
    ques['Answer'].values[ques['Answer'].str.len() <150 ] = ""
    
    
    
    
    ques=ques[ques.iloc[:,1]=="NO"]
    ques.iloc[:,0]=ques.QUES.str.capitalize()
    counter=len(ques)-1
    
    
    
    execut=0
    
    while (counter>=0):
        time.sleep(3)
    
        try:
            login=browser.find_element_by_xpath("/html/body/div[1]/div/div/div[2]/div/div/div[5]/div/div/div/div/div")
            
#            login=browser.find_element_by_css_selector(".AskQuestionButton.LookupBarAskQuestionModalButton")
            login.click()
                
            time.sleep(2)
                
            keyboard.type(ques.iloc[counter,0])
            ques.iloc[counter,1]="YES"
            time.sleep(2)
#            browser.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/div[2]/div/div/div/div/div/div").click()
#            browser.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/div[2]/div/div/div/div/div[2]/div/div/div[1]/div/div/div[3]/div[1]/div").click()

            
            login=browser.find_element_by_css_selector(".submit_button.modal_action")
            time.sleep(1)

#            login=browser.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/div/div/div[2]/div/div/div[2]/div/div[2]/div/div/div/div/div")
#            
#            login=browser.find_element_by_css_selector(".AskQuestionButton.LookupBarAskQuestionModalButton")
            login.click()
            
#            login=browser.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[3]/div/span[2]/a")
#            login.click()
            try:
                time.sleep(3)
                login=browser.find_element_by_css_selector(".submit_button.modal_action")

#                login=browser.find_element_by_xpath("/html/body/div[3]/div/div[1]/div[2]/div/div/div[2]/div/div/div[3]/div/div[2]/div/div/div/div/div")
            
#            login=browser.find_element_by_css_selector(".AskQuestionButton.LookupBarAskQuestionModalButton")
                login.click()
#                login=browser.find_element_by_xpath("/html/body/div[2]/div[2]/div/div[3]/div/span[2]/a")
#            
##               login=browser.find_element_by_css_selector(".AskQuestionButton.LookupBarAskQuestionModalButton")
#                login.click()
                time.sleep(3)
                click(300,700)
                time.sleep(2)
                ques.to_csv(r'C:\Users\Ranjith James\Documents\output.csv',index=False)
                execut=1
    
    #            if(login!=[]):
    #                time.sleep(2)
    #                keyboard.press(Key.tab)
    #                time.sleep(1)
    #                keyboard.press(Key.tab)
    #                time.sleep(1)
    #                keyboard.press(Key.tab)
    #                time.sleep(1)
    #                keyboard.press(Key.enter)
    #                keyboard.release(Key.enter)
            except:
                time.sleep(2)
                click(300,700)
                time.sleep(2)
                ques.to_csv(r'C:\Users\Ranjith James\Documents\output.csv',index=False)
                execut=1
            if(execut==12222 ): 
                if(ques.iloc[counter,2]!="" and cout<100):
                    browser.get("http://www.quora.com")    
                    time.sleep(2)  
                    login=browser.find_element_by_xpath("/html/body/div[4]/div[5]/div/div/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div/div[4]/div/div[3]/div/div/div/div[1]/div[1]/span/a")
                    login.click()
                    time.sleep(2)
                    keyboard.type(ques.iloc[counter,2])
                    cout=cout+1
                    time.sleep(2)
                    login=browser.find_element_by_xpath("/html/body/div[4]/div[5]/div/div/div/div[2]/div[2]/div[2]/div[1]/div[1]/div/div/div[2]/div/div/div/div[4]/div/div[3]/div/div/div/div[2]/div/div/div[1]/div[2]/div[3]/div[2]/div/div[2]/div/a")
                    login.click()
                    time.sleep(2)
            browser.get("http://www.quora.com")
            time.sleep(2)
            counter=counter-1
            execut=999
        except:
            click(300,700)
            time.sleep(2)
            ques.to_csv(r'C:\Users\Ranjith James\Documents\output.csv',index=False)
            counter=counter-1
            execut=0
            browser.get("http://www.quora.com")    
            time.sleep(2)
    browser.close()
        
        
        
    
        
        
    
    
    browser.get("https://www.quora.com/partners")
    time.sleep(4)
    
    from selenium.webdriver.common.by import By
    s=browser.find_elements(By.CSS_SELECTOR, '.ui_button.u-nowrap.ui_button--styled.ui_button--FlatStyle.ui_button--FlatStyle--blue.ui_button--size_regular.u-inline-block.ui_button--non_link.ui_button--supports_icon.ui_button--has_icon.ui_button--icon_only')
    
    
    for i in range(0,500):
        time.sleep(2)
        try:
         s[i].click()
        except:
         s=browser.find_elements(By.CSS_SELECTOR, '.ui_button.u-nowrap.ui_button--styled.ui_button--FlatStyle.ui_button--FlatStyle--blue.ui_button--size_regular.u-inline-block.ui_button--non_link.ui_button--supports_icon.ui_button--has_icon.ui_button--icon_only')
        time.sleep(4)
        abc=2
        for y in range(0,3):
            try:
                login=browser.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div[1]/div/div["+str(abc)+"]/div/div/div[3]/div/div/div/span")
                login.click()                       
                abc=abc+1
                time.sleep(0.2)
            except:
                print("will try next time")      
        click(300,700)
    
        
    browser.get("https://www.quora.com/partners?sort_by=week#questions")
    time.sleep(4)
    
    from selenium.webdriver.common.by import By
    s=browser.find_elements(By.CSS_SELECTOR, '.ui_button.u-nowrap.ui_button--styled.ui_button--FlatStyle.ui_button--FlatStyle--blue.ui_button--size_regular.u-inline-block.ui_button--non_link.ui_button--supports_icon.ui_button--has_icon.ui_button--icon_only')
    
    
    for i in range(0,100):
        time.sleep(2)
        try:
         s[i].click()
        except:
         s=browser.find_elements(By.CSS_SELECTOR, '.ui_button.u-nowrap.ui_button--styled.ui_button--FlatStyle.ui_button--FlatStyle--blue.ui_button--size_regular.u-inline-block.ui_button--non_link.ui_button--supports_icon.ui_button--has_icon.ui_button--icon_only')
        time.sleep(4)
        abc=2
        for y in range(0,6):
            try:
                login=browser.find_element_by_xpath("/html/body/div[3]/div/div[1]/div/div/div/div[2]/div/div/div[2]/div[3]/div[2]/div[1]/div/div["+str(abc)+"]/div/div/div[3]/div/div/div/span")
                login.click()                       
                abc=abc+1
                time.sleep(0.2)
            except:
                print("will try next time")      
        click(300,700)
    
    
    
    
    
