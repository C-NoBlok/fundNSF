import xml.etree.ElementTree as ET
import pandas as pd
import urllib.request
import requests
import bs4 as bs
import io

class FundNSF:
    def __init__(self):
        self.nsf_api = 'http://api.nsf.gov/services/v1/awards.xml?'
        a_id = None
        award_id_api = 'http://api.nsf.gov/services/v1/awards/{}.xml?'.format(a_id)
        self.page_count = 1 #can only pull 25 records at a time

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
        '''takes list of keywords to search nsf awards database for

        get_keywords_data(['keywords'],
                            abstractText=False)
            return data_dictionary
        '''

        self.reset_fields()
        for key, value in kwargs.items():
            self.fields[key] = value
        request_url = self.assemble_url(keywords)
        print(request_url)

        self.xml_files = self.send_request_xml(request_url)
        self.data = self.construct_data_xml(self.xml_files)

        return self.data

    def assemble_url(self, keywords):
        '''Takes dictionary of search parameters and returns a request urllib

        assemble_url(param_dict)
            return('request_url')
        '''

        include = []
        for field in self.fields:
            if self.fields[field] == True:
                include.append(field)
        include = ','.join(include)
        keywords = '+'.join(keywords)
        request_url = \
            self.nsf_api + 'keyword=' + keywords + '&printFields=' + include
        return request_url

    def send_request_xml(self, request_url):
        '''sends request to NSF Database and returns xml file object

        send_request('request_url')
            return xml_file_obj
        '''
        xml_files = []
        page_count = 1

        if page_count == 1:
            r = requests.get(request_url)
            xml_file = io.StringIO(r.text)
            xml_files.append(xml_file)

        tree = ET.parse(xml_file)
        root = tree.getroot()
        print(print('collecting page: {}'.format(page_count)))
        print('Entries Found: {}'.format(len(root)))
        page_count += 1
        while len(root)%25 == 0 and len(root)>0:
            print(request_url + '&offset={}'.format(page_count))
            r = requests.get(request_url + '&offset={}'.format(page_count))
            xml_file = io.StringIO(r.text)
            xml_files.append(xml_file)
            tree = ET.parse(xml_file)
            root = tree.getroot()
            xml_file.seek(0)
            for response in root:
                #print(len(response))
                for award in response:
                    #print(award.tag + ': ' + award.text)
                    pass
            page_count += 1

            print(print('collecting page: {}'.format(page_count)))
            print('Entries Found: {}'.format(len(root)))


        return xml_files

    def construct_data_xml(self, xml_file_list):
        '''Parses list of .xml data file objects using xml.eTree.ElementTree package returns
        dictionary of values.

        *Optional: pass dictionary to append_to keyward add

        construct_data_xml(xml_data, dict_to_append_to)
            returns dictionary
        '''
        award_dict = {}
        for xml_file in xml_file_list:
            print(xml_file)
            xml_file.seek(0)
            tree = ET.parse(xml_file)
            root = tree.getroot()
            #print(root.tag)
            for response in root:
                #print(len(response))
                for award in response:
                    #print(award.tag + ': ' + award.text)
                    try:
                        award_dict[award.tag].append(award.text)
                    except KeyError as e:
                        award_dict[award.tag] = [award.text]

        return award_dict

    def reset_fields(self):
        '''Resets the parameter field dictionary back to default

        reset_fields()
            return None
        '''
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
    test_url = 'http://api.nsf.gov/services/v1/awards.xml?keyword=hysitron&printFields=id,title,agency,awardeeCity,awardeeName,awardeeStateCode,date,fundsObligatedAmt,piFirstName,piLastName'
    nsf = FundNSF()
    files = nsf.send_request_xml(test_url)
    data = nsf.get_keyword_data(['hysitron'], abstractText=False)
    df = pd.DataFrame(data)
    print(df.head())









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
