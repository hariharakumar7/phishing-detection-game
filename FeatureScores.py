class FeatureScores:
	
	def __init__(self ):
		
		self.HTTPSPresent = -3
		self.HTTPSPresent_time = -3
		
		self.DomainLength = -3
		self.DomainLength_time = -3
		
		self.DomainName = ""
		self.DomainSuffix = ""
		self.DomainName_time = -3
		
		self.DomainRank = -3
		self.DomainRank_time= -3
		
		
		self.NonAlphabetical = -3
		self.NonAlphabetical_time= -3
		
		self.CopyRightLogo = -3
		self.CopyRightLogo_time= -3
		
		self.OutsideRationInHeader = -3
		self.OutsideRationInHeader_time= -3

		self.OutsideRationInBody = -3
		self.OutsideRationInBody_time= -3
		
		self.TitleContainDomainName = -3
		self.IsEnglish = -3
		
		self.Title =""
		self.url = ""
		self.label = ""
		self.index = ""
		self.alexa_rank = "" 
		self.source = ""
		self.siteHTML = ""
		self.sitePlain = ""
		
	@staticmethod
	def getHeader ():
		return ( 'HTTPSPresent , HTTPSPresent_time , DomainLength  , DomainLength_time ,  DomainName , DomainSuffix , DomainName_time , DomainRank ,  DomainRank_time , NonAlphabetical , NonAlphabetical_time , CopyRightLogo , CopyRightLogo_time , OutsideRationInHeader , OutsideRationInHeader_time, OutsideRationInBody , OutsideRationInBody_time , TitleContainDomainName , IsEnglish , Title , url  , label , index , alexa_rank , source ' )
		
        #return ( 'HTTPSPresent , DomainLength  ,  DomainRank , NonAlphabetical  , CopyRightLogo  , OutsideRationInHeader  , OutsideRationInBody , DomainName , DomainSuffix ,  label , alexa_rank , source , url ' )
		
	def getScores(self):
		res = '{} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} , {} '.format( self.HTTPSPresent , self.HTTPSPresent_time , self.DomainLength  , self.DomainLength_time ,  self.DomainName , self.DomainSuffix , self.DomainName_time , self.DomainRank , self.DomainRank_time , self.NonAlphabetical , self.NonAlphabetical_time , self.CopyRightLogo , self.CopyRightLogo_time , self.OutsideRationInHeader , self.OutsideRationInHeader_time, self.OutsideRationInBody , self.OutsideRationInBody_time , self.TitleContainDomainName , self.IsEnglish , self.Title , self.url , self.label , self.index , self.alexa_rank , self.source , self.siteHTML , self.sitePlain  )
		
		return res
		
		
