import xml.etree.ElementTree as ET
import pandas as pd
import urllib.request
import bs4 as bs

class FundNSF:
    def __init__(self):
        self.nsf_api = 'http://api.nsf.gov/services/v1/awards.xml?'
        a_id = None
        award_id_api = 'http://api.nsf.gov/services/v1/awards/{}.xml?'.format(a_id)
        parameters = ['printFields=abstractText',
                        'keyword=nano']



        self.fields = {
        'id': True,
        'title': True,
        'agency' : True,
        'awardeeCity' : True,
        'awardeeName' : True,
        'awardeeStateCode' : True,
        'date' : True,
        'fundsObligatedAmt' : True,
        'piFirstName' : True,
        'piLastName' : True,
        'abstractText' : False,
        'startDate' : False,
        'expDate' : False,
        'fundProgramName' : False
        }


    def get_keyword_data(self, keywords, **kwargs):
        '''Provide list of keywords to search nsf awards database for
        get_keywords_data(['keywords'],
                            abstractText=False)
        '''

        self.reset_fields()
        for key, value in kwargs.items():
            self.fields[key] = value
            print(self.fields[key])

        include = []
        for field in self.fields:
            if self.fields[field] == True:
                include.append(field)
        include = ','.join(include)
        keywords = '+'.join(keywords)
        request_url = \
            self.nsf_api + 'keyword=' + keywords + '&printFields=' + include
        print(request_url)

        self.xml = self.send_request(request_url)
        self.data = self.construct_data(self.xml)
        return self.data



    def send_request(self, request_url):
        '''Sends request to NSF Data base and returns a bs4.BeautifulSoup object
        send_request('request_url')
            return bs4.BeautifulSoup() #should be an xml file
        '''

        self.sauce = urllib.request.urlopen(request_url).read()
        return bs.BeautifulSoup(self.sauce, 'lxml')

    def construct_data(self, xml_data):
        return_dict = {}
        for field in self.fields:
            if self.fields[field] == True:
                return_dict[field] = xml_data.find_all(field)
                return_dict[field] = [field.text for field in return_dict[field]]

        return return_dict

    def reset_fields(self):
        self.fields = {
            'id': True,
            'title': True,
            'agency' : True,
            'awardeeCity' : True,
            'awardeeName' : True,
            'awardeeStateCode' : True,
            'date' : True,
            'fundsObligatedAmt' : True,
            'piFirstName' : True,
            'piLastName' : True,
            'abstractText' : False,
            'startDate' : False,
            'expDate' : False,
            'fundProgramName' : False
        }






if __name__ == '__main__':
    nsf = FundNSF()

    data = nsf.get_keyword_data(['nano', 'hysitron', 'Reno', '1126582'], abstractText=True)
    xml = nsf.xml
    #titles = xml.find_all('title')
    #titles = [title.text for title in titles]
    #print(titles)
    print([key + ': ' + str(len(data[key])) for key in data.keys()])

    for child in xml.children:
        continue




#Printable Fields
'''
rpp
offset
id (*)
agency (*)
awardeeCity (*)
awardeeCountryCode
awardeeCounty
awardeeDistrictCode
awardeeName (*)
awardeeStateCode (*)
awardeeZipCode
cfdaNumber
coPDPI
date (*)
startDate
expDate
estimatedTotalAmt
fundsObligatedAmt (*)
dunsNumber
fundProgramName
parentDunsNumber
pdPIName
perfCity
perfCountryCode
perfCounty
perfDistrictCode
perfLocation
perfStateCode
perfZipCode
poName
primaryProgram
transType
title (*)
awardee
poPhone
poEmail
awardeeAddress
perfAddress
publicationResearch
publicationConference
fundAgencyCode
awardAgencyCode
projectOutComesReport
abstractText
piFirstName (*)
piMiddeInitial
piLastName (*)
piPhone
piEmail
'''
