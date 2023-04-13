import selenium
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
import time
import os
import sqlite3
import datetime
import numpy as np 
k=0
connect = sqlite3.connect("whalesActivity.db")
cursor = connect.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Whales(Recorded_Time INT PRIMARY KEY, 
						  transaction_time INT, crypto_amount INT, crypto_type TEXT, 
						  dollar_worth INT, type_of_transaction TEXT, Sender TEXT,
						  Receiver TEXT);''')
connect.commit()
items=[]
insert_query = """INSERT INTO Whales VALUES(?, ?, ?, ?, ?, ?, ?, ?)"""
driver = webdriver.Chrome(executable_path='/chromedriver_linux64/chromedriver')
driver.get('https://whale-alert.io')
time.sleep(1)
element = driver.find_element(By.ID, "term-container")
time.sleep(0.1)
i=1
span_prev = ""
span_akt = ""
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tx")))
spans = driver.find_elements(By.CLASS_NAME, "tx")
time.sleep(0.01)
j=0
if j==0:
	for i in range(len(spans)):
		print(spans[i].text)
j=1
while (j==1):
	if k==0:
		spans = driver.find_elements(By.CLASS_NAME, "tx")
		for i in range(len(spans)):
			print(spans[i].text)
	connect = sqlite3.connect("whalesActivity.db")
	connect.commit()
	cursor = connect.cursor()
	element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "tx")))
	spans = driver.find_elements(By.CLASS_NAME, "tx")
	span_akt = spans[len(spans)-2]
	if span_akt != span_prev:
		datas = span_akt.text.split()
		print(datas)
		if datas[0] != "Fetching":
			items.append(datetime.datetime.now())
			transaction_time = datas[0]
			items.append(transaction_time)
			crypto_amount = datas[1]
			items.append(crypto_amount)
			crypto_type = datas[2]
			items.append(crypto_type)
			dollar_worth = datas[3] + datas[4]
			items.append(dollar_worth)
			type_of_transaction = datas[5]
			items.append(type_of_transaction)
			try:
				from_index = datas.index("from")
				to_index = datas.index("to")
			except:
				pass
			sender = ""
			try:
				for k in range((from_index+1), (to_index)):
					sender = sender + datas[k]
			except:
				pass
			receiver = ""
			try:
				for k in range((to_index+1), len(datas)):
					receiver = receiver + datas[k]
			except:
				pass
			items.append(sender)
			items.append(receiver)
			cursor.execute(insert_query, items)
			connect.commit()
			connect.close()
			items=[]
		with open("whaleActivity.txt", "a") as file:
			file.write("\n")
			file.write(span_akt.text)
	k=k+1
	span_prev = span_akt
	connect.close()
	if k==200:
		driver.refresh()
		time.sleep(1)
		k=0
