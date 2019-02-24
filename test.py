import sys

class DevNull:
    def write(self, msg):
        pass

sys.stderr = DevNull()
import requests
from Extract import *
import pickle
from bs4 import BeautifulSoup
import urllib.request

class check():
	url=""
	def __init__(self,x):
		url=x
	def evaluatee(self):
		page = requests.get(self.url)
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
		if predict==0:
			print("Phishing Website")
		else:
			print("Legitimate site")
