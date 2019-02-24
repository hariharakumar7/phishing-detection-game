import sys


class DevNull:
    def write(self, msg):
        pass

sys.stderr = DevNull()
import tkinter
import requests
from Extract import *
import pickle
import numpy as np
from bs4 import BeautifulSoup
import urllib.request
def evaluatee(url):
	page = requests.get(url)
	soup = BeautifulSoup(page.content, 'html.parser')
	rs=soup.prettify()
	r=rs.encode()
	e=Extract(url,"test",1,rs,1,rs,rs)
	e.DoEvaluate()
	abc=0
	if(b'\xc2\xa9' in r):
	     abc=1
	else:
		abc=0
	#print(e.phishScore.DomainName)
	links=soup.find_all("a")
	c=0
	for i in links:
		if e.phishScore.DomainName in links:
			c+=1
	title=-1
	if e.phishScore.DomainName in soup.find_all("title"):
		title=1

	X=[e.phishScore.HTTPSPresent,e.phishScore.DomainLength,e.phishScore.NonAlphabetical,rs.count(e.phishScore.DomainName),e.phishScore.OutsideRationInBody,abc,title]#e.phishScore.TitleContainDomainName]
	X=np.array(X)
	X=X.reshape(1,-1)

	classifier = pickle.load(open("phishing_model.pkl", 'rb'))
	predict=classifier.predict(X)
	#print(predict)
	return predict

	if predict==0:
		print("Phishing Website")
	else:
		print("Legitimate site")

# code to retrieve a random record from the dataset

import pandas as pd
import random
data=pd.read_csv("features.csv")
YY=data.values
YY=YY[:,[0,2]]
n=len(YY)-1

# UI for the entire program
from tkinter import *

scores=0
flag=1

root = Tk()
root.title("Phishing Detection Game")

answer_label =Label(root, text ="Solution Appears Here!")
answer_label.grid(row =0, column =0,pady=10)

score=Label(root,text="Score: 0")
score.grid(row=0,column=1,pady=10)

label1 =Label(root, text ="https://www.google.com")
label1.grid(row =1, column =0,pady=10,padx=10)

num1_txtbx =Entry(root)
num1_txtbx.grid(row =1, column =1,padx=10)

def addF():
	global scores,flag
	if flag==0:
		return
	answer_label.configure(text="Please Wait!")
	pred=evaluatee(label1["text"])
	if str(pred[0])==num1_txtbx.get().strip():
		predi="Correct Answer! :)"
		if flag==1:
			scores+=1
	else:
		predi="Wrong Answer :("

	answer_label.configure(text=predi)
	score.configure(text="Score: "+str(scores))
	flag=0

def next():
	global flag
	flag=1
	num1_txtbx.delete(0,END)
	num1_txtbx.insert(0,"")
	rec=["5"*150,0]
	while len(rec[0])>100:
		ran=random.randint(0,n-1)
		rec=YY[ran]
	label1.configure(text=rec[0])
	answer_label.configure(text="Solution Appears Here!")


calculate_button =Button(root, text="Check!!", command= addF)
calculate_button.grid(row =3, column =0, columnspan =2,pady=10)

next_button =Button(root, text="Next Website",command=next)
next_button.grid(row =4, column =0, columnspan =2,pady=10)

label2 =Label(root, text ="Enter 1 for Legitimate website and 0 for Phishing website")
label2.grid(row =5, column =0,pady=10,columnspan=2)


root.mainloop()
