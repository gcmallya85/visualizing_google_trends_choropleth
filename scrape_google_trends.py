# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 2018

@author: gmallya
"""
# The script below assumes you have Chrome Driver downloaded (make necessary changes if you are using other WebDrivers)
# Please make necessary changes to directory paths mentioned in the script


### Download data from Google Trends (Data is downloaded to default downloads folder set in Chrome)
webdriver_path = 'C:\Users\gmallya\Downloads\chromedriver.exe'
search_term = "cookies"

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
states = ["AL","AK","AZ","AR","CA","CO","CT","DE","DC","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"]     
my_xpath = "/html[1]/body[1]/div[2]/div[2]/div[1]/md-content[1]/div[1]/div[1]/div[4]/trends-widget[1]/ng-include[1]/widget[1]/div[1]/div[1]/div[1]/widget-actions[1]/div[1]/button[1]/i[1]" # Comes from Chrome plugin ChroPath 
driver = webdriver.Chrome(executable_path=webdriver_path) # Open Chrome Browser
for st in states:
    time.sleep(5) # Wait for browser to open
    url = "https://trends.google.com/trends/explore?date=all&geo=US-"+st+"&q="+search_term # update the query URL
    driver.get(url) # ping the URL of interest
    driver.refresh() # Refresh the page (To circumvent Error: 429)
    try:
        element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, my_xpath)))
        driver.find_element_by_xpath(my_xpath).click() #Download the csv file by mimicking the click
    finally:
        if not element:
            print "Could not download data for : "+st
        time.sleep(2)
driver.quit()

### Data Processing
import glob
import os
state_ids = [1,2,4,5,6,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56]
states_fullnames =["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","District of Columbia","Florida","Georgia","Hawaii","Idaho","Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah","Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]
downloaded_files = (sorted(glob.glob("C:\\Users\\gmallya\\Downloads\\relatedQ*.csv"), key=os.path.getmtime))

# Details about the most popular queries
top_query = []
top_query_file_name = "C:\\Users\\gmallya\\Downloads\\top_query.csv"
top_query_only_file = open(top_query_file_name,'w')
top_query_line = "State,Query,Class\n"
top_query_only_file.write(top_query_line)

# Details about all queries in a state
top_queries_full = []
top_queries_full_file_name = "C:\\Users\\gmallya\\Downloads\\top_queries_full.csv"
top_queries_full_file = open(top_queries_full_file_name,'w')
top_queries_full_line = "StateID,Query,Prct\n"
top_queries_full_file.write(top_queries_full_line)


for fn in downloaded_files:
    top = 0
    rising = 0
    with open(fn) as f:
        for i,line in enumerate(f):
#            print "line {0} = {1}".format(i,line)
            if i >= 1: # All RELEVANT entries in the CSV file begin at line number 2 (in python 1)
                if i == 1:  # Line 2 has state entry
                    st_name = line.split(",")[-1].split(")")[0].replace(" ","_")
                else:
                    if ("RISING" in line) or rising == 1:
                        if rising == 0: # Define the output filename and open it in write mode
                            output_file_name = "C:\\Users\\gmallya\\Downloads\\rising"+st_name+".csv"
#                            print output_file_name
                            file = open(output_file_name,'w')
                        rising = 1
                        top = 0
                        if "cookie" in line: # Add entry to output file only if there is substring called cookie(s)
                            file.write(line)
                        
                    if ("TOP" in line) or top == 1:
                        if top == 0: # Define the output filename and open it in write mode
                            new_line = 1 # to track the top query
                            output_file_name = "C:\\Users\\gmallya\\Downloads\\top"+st_name+".csv"
                            file = open(output_file_name,'w')
                        top = 1
                        rising = 0
                        if ("cookie" in line) and ("recipe" not in line): # Add entry to output file only if there is substring called cookie(s)
                            file.write(line) # Write queries into individual files
                            # Write all queries into a single file
                            top_queries_full_line = str(state_ids[states_fullnames.index(st_name[1:].replace("_"," "))])+","+line
                            top_queries_full_file.write(top_queries_full_line)
                            if new_line == 1: # To track the top query
                                new_line = 0
                                top_query.append(line.split(",")[0])
                                myset = set(top_query)
#                                print myset
                                mylist = list(myset)
#                                top_query_line = st_name[1:].replace("_"," ")+","+line.split(",")[0]+","+str(mylist.index(line.split(",")[0]))+"\n"
#                                top_query_only_file.write(top_query_line)
                    if line == [] and (rising == 1 or top == 1):
                        file.close()              
top_queries_full_file.close()
file.close()


# Run seperately to fix switching position of queries in myset
# populate a file with top queries only
for fn in downloaded_files:
    top = 0
    with open(fn) as f:
        for i,line in enumerate(f):
#            print "line {0} = {1}".format(i,line)
            if i >= 1: # All RELEVANT entries in the CSV file begin at line number 2 (in python 1)
                if i == 1:  # Line 2 has state entry
                    st_name = line.split(",")[-1].split(")")[0].replace(" ","_")
                else:
                    if ("TOP" in line) or top == 1:
                        if top == 0: # Define the output filename and open it in write mode
                            new_line = 1 # to track the top query
                            
                        top = 1
                        if ("cookie" in line) and ("recipe" not in line): # Add entry to output file only if there is substring called cookie(s)
                            if new_line == 1: # To track the top query
                                new_line = 0
                                top_query_line = st_name[1:].replace("_"," ")+","+line.split(",")[0]+","+str(mylist.index(line.split(",")[0]))+"\n"
                                top_query_only_file.write(top_query_line)
top_query_only_file.close()

#myset = set(top_query)
print myset