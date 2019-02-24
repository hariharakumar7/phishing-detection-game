from FeatureScores import FeatureScores

import tldextract
from timeit import default_timer as timer
import re
import numpy as np
from bs4 import BeautifulSoup, SoupStrainer

class Extract:
	"""This class takes in a url and retrieves data about the web page"""


	def __init__(self , url , label , index , source , alexa_rank , siteHTML , sitePlain):
		
		# the URL we are testing
		# self.total_feature_number = 30
		self.phishScore = FeatureScores()

		self.phishScore.url = url.lower()
		self.phishScore.label = label
		self.phishScore.index = index
		self.phishScore.alexa_rank = alexa_rank 
		self.phishScore.source = source
		self.phishScore.siteHTML = siteHTML.lower()
		self.phishScore.sitePlain = sitePlain
		
	def DoEvaluate(self ):

		
		start = timer()
		self.phishScore.HTTPSPresent = self.HTTPSPresent(self.phishScore.url)
		self.phishScore.HTTPSPresent_time= (timer()  - start) 
		
		start = timer()
		self.phishScore.DomainLength = self.DomainLength(self.phishScore.url)
		self.phishScore.DomainLength_time= (timer()  - start) 
		
		start = timer()
		self.phishScore.DomainName , self.phishScore.DomainSuffix  = self.DomainName(self.phishScore.url)
		self.phishScore.DomainName_time= (timer()  - start) 
		
		start = timer()
		self.phishScore.DomainRank = self.DomainRank( self.phishScore.sitePlain , self.phishScore.DomainName)
		self.phishScore.DomainRank_time= (timer()  - start) 
		
		start = timer()
		self.phishScore.NonAlphabetical = self.NonAlphabetical(self.phishScore.DomainName)
		self.phishScore.NonAlphabetical_time= (timer()  - start)
		
		start = timer()
		self.phishScore.CopyRightLogo = 0#self.CopyRightLogo( self.phishScore.siteHTML , self.phishScore.DomainName)
		self.phishScore.CopyRightLogo_time= (timer()  - start)
		
		start = timer()
		self.phishScore.OutsideRationInHeader = self.OutsideRationInHeader(self.phishScore.siteHTML , self.phishScore.DomainName , self.phishScore.DomainSuffix )
		self.phishScore.OutsideRationInHeader_time= (timer()  - start) 
		
		start = timer()
		self.phishScore.OutsideRationInBody = self.OutsideRationInBody(self.phishScore.siteHTML , self.phishScore.DomainName , self.phishScore.DomainSuffix )
		self.phishScore.OutsideRationInBody_time= (timer()  - start)
		
		start = timer()
		self.phishScore.TitleContainDomainName , self.phishScore.Title , self.phishScore.IsEnglish = self.TitileContainsDomainName(self.phishScore.siteHTML , self.phishScore.DomainName )
		self.phishScore.Title_time= (timer()  - start)
		

	def HTTPSPresent(self , url):
		if (url[:5].lower() == 'https'):
			#print(url[:5].lower())
			return 1
		
		if (url[:4].lower() == 'http'):
			return -1
			
		return -2
		
	def DomainLength (self , url):
		
		tldObj = tldextract.extract(url)
		
		if (len(tldObj.domain)) > 0 :
			return (len(tldObj.domain))
		else:
			return -2

	def DomainName (self , url):
		tldObj = tldextract.extract(url)
		domain=url.split("//www.")[-1].split("/")[0].split(".")[0]
		if (len(tldObj.domain)) > 0 :
			return domain , tldObj.suffix
		else:
			return ""

	def DomainRank( self , sitePlain  , DomainName):
		DomainName = DomainName.lower()
		sitePlain = ' '.join(sitePlain)
		sitePlain = sitePlain.replace(' ' , '')
		sitePlain = sitePlain.lower()
		cnt = sitePlain.count(DomainName)
		return 0

	def NonAlphabetical(self , DomainName ):
		s = re.sub('[a-zA-Z]+', '', DomainName)
		if len(s) > 0:
			return 1
		else:
			return -1

	def CopyRightLogo( self , siteHTML  , DomainName):
		
		lstPositions = []
		
		lstSigns = [ '&trade;' , '&#8482;' , '&#x2122;' ,  '&#8471;' , '&#x2117;' , '&#169;' , '&#x00A9;' , '&copy;' , '&#174;' , '&#x00AE;' , '&reg;' , '&#174;'  ]
		for sign in lstSigns:
			pos = siteHTML.lower().find(sign)
			if ( pos > -1 ):
				lstPositions.append(pos)
		
		#print (lstPositions)
		
		if (len (lstPositions) ) == 0:
			return 0
		
		#print (lstPositions)
		
		for pos in lstPositions:
			
			startOffset = 0
			endOffset = len (siteHTML)
			desiredLen = 50
			
			if ( pos - desiredLen ) > 0 :
				startOffset = pos - desiredLen
			if ( pos + desiredLen ) < len (siteHTML) :
				endOffset = pos + desiredLen
				
			copyRightPart =	siteHTML[startOffset:endOffset]
			copyRightPart = copyRightPart.replace(" ", "").lower()
			#print copyRightPart
			if ( copyRightPart.find(DomainName.lower()) > 0 ):
				#print ('found')
				return -1
			
		return 1
		

	def OutsideRationInHeader(self , siteHTML , DomainName , DomainSuffix):
		positiveAnchor = 0
		negativeAnchor = 0
		for link in BeautifulSoup(siteHTML, parseOnlyThese=SoupStrainer('a')):
			if link.has_key('href'):
				tldObj = tldextract.extract(link['href'])
				if (tldObj.domain == DomainName and tldObj.suffix == DomainSuffix):
					positiveAnchor += 1
				else:
					negativeAnchor += 1
		if (positiveAnchor + negativeAnchor == 0):
			return 0
		else:
			return round( 1 - float(negativeAnchor) / (positiveAnchor + negativeAnchor), 2)

	def OutsideRationInBody(self , siteHTML , DomainName , DomainSuffix):
		positiveAnchor = 0
		negativeAnchor = 0
		for link in BeautifulSoup(siteHTML, parseOnlyThese=SoupStrainer(['meta', 'script', 'link'])):
			if link.has_key('href'):
				tldObj = tldextract.extract(link['href'])
				if (tldObj.domain == DomainName and tldObj.suffix == DomainSuffix):
					positiveAnchor += 1
				else:
					negativeAnchor += 1
		if (positiveAnchor + negativeAnchor == 0):
			return 0
		else:
			return round( 1 - float(negativeAnchor) / (positiveAnchor + negativeAnchor), 2)

	def TitileContainsDomainName(self , siteHTML , DomainName ):
		siteHTML = siteHTML.lower()
		if ((siteHTML.find('<title>') >= 0 ) and (siteHTML.find('</title>') >= 0 ) ):
			title = str(siteHTML).split('<title>')[1].split('</title>')[0]
			title = title.lower()
			
			regex = re.compile('[^a-zA-Z]')
			title = regex.sub('', title)
			DomainName = regex.sub('', DomainName)
			
			IsEnglish = -1
			s = re.sub('[a-zA-Z]+', '', title)
			if len(s) > 0:
				IsEnglish = 1
			
			#print ("Title = " , title)
			pos = title.find(DomainName)
			if ( pos >= 0  ):
				return -1 , title , IsEnglish
			else:
				return 1 , title , IsEnglish
		else:
			return 0 , "" , 0
		
	

	def PrintReadyScores(self):
		return self.phishScore.getScores()

	@staticmethod
	def getHeader():
		return FeatureScores.getHeader()