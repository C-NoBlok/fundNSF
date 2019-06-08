"""
Perform searches on the National Science Foundationsawards database.

https://www.research.gov/common/webapi/awardapisearch-v1.htm

-------------
Example
-------------
import fundNSF
import pandas as pd

nsf = FundNSF()
nsf.set_fields(abstractText=True)
nsf.set_params(dateStart='01/01/2017',
                dataEnd='12/31/2017') # enter date as 'mm/dd/yyyy'
data = nsf.keyword_search('nano') #returns a Dictionary
df = pd.DataFrame(data)
print(df.head())

award_data = nsf.id_search(df['id'][0])
print(award_data['abstractText'])
"""

import xml.etree.ElementTree as ET
# import urllib.request
import requests
import io


class FundNSF:
    """
    Perform searches on the National Science Foundationsawards database.

    https://www.research.gov/common/webapi/awardapisearch-v1.htm

    -------------
    Example
    -------------
    import fundNSF
    import pandas as pd

    nsf = FundNSF()
    nsf.set_fields(abstractText=True)
    nsf.set_params(dateStart='01/01/2017',
                    dataEnd='12/31/2017') # enter date as 'mm/dd/yyyy'
    data = nsf.keyword_search('nano') #returns a Dictionary
    df = pd.DataFrame(data)
    print(df.head())

    award_data = nsf.id_search(df['id'][0])
    print(award_data['abstractText'])
    """

    def __init__(self):
        """Construct FundNSF() Object."""
        self.nsf_api = 'http://api.nsf.gov/services/v1/awards.xml?'
        self.fields = {
            'offset': False,
            'id': True,
            'agency': True,
            'awardeeCity': True,
            'awardeeCountryCode': False,
            'awardeeCounty': False,
            'awardeeDistrictCode': False,
            'awardeeName': True,
            'awardeeStateCode': True,
            'awardeeZipCode': False,
            'cfdaNumber': False,
            'coPDPI': False,
            'date': True,
            'startDate': False,
            'expDate': False,
            'estimatedTotalAmt': False,
            'fundsObligatedAmt': True,
            'dunsNumber': False,
            'fundProgramName': False,
            'parentDunsNumber': False,
            'pdPIName': False,
            'perfCity': False,
            'perfCountryCode': False,
            'perfCounty': False,
            'perfDistrictCode': False,
            'perfLocation': False,
            'perfStateCode': False,
            'perfZipCode': False,
            'poName': False,
            'primaryProgram': False,
            'transType': False,
            'title': True,
            'awardee': False,
            'poPhone': False,
            'poEmail': False,
            'awardeeAddress': False,
            'perfAddress': False,
            'publicationResearch': False,
            'publicationConference': False,
            'fundAgencyCode': False,
            'awardAgencyCode': False,
            'projectOutComesReport': False,
            'abstractText': False,
            'piFirstName': True,
            'piMiddeInitial': False,
            'piLastName': True,
            'piPhone': False,
            'piEmail': False
        }

        self.params = {
            'offset': None,  # Record offset -> page cfdaNumber
            'agency': None,  # 'NSF' or 'NASA'
            # Start date for award date to search (ex. 12/31/2012)
            'dateStart': None,
            'dateEnd': None,  # End date for award date to search mm/dd/yyyy
            # Start date for award start date to search
            'startDateStart': None,
            'startDateEnd': None,  # End date for award start date to search
            'expDateStart': None,  # start date for award exp date to search
            'expDateEnd': None,  # end date for award exp date to search
            'estimatedTotalAmtFrom': None,
            'estimatedTotalAmtTo': None,
            'estimatedObligatedAmtFrom': None,
            'estimatedObligatedAmtTo': None,
            'awardeeStateCode': None,
            'awardeeName': None,
            'awardeeCountryCode': None,
            'awardeeCounty': None,  # VA01, NY22
            'awardeeDistrictCode': None,
            'fundsObligatedAmtFrom': None,
            'fundsObligatedAmtTo': None,
            'estimatedTotalAmtFrom': None,
            'estimatedTotalAmtTo': None,
            'dunsNumber': None,
            'primaryProgram': None,
            'projectOutcomesOnly': None,
            'pdPIName': None
        }

    def get_awards_from(self, start_date):
        """
        Get all awards from start_date to present
        :param start_date: string in the form of 'mm/dd/yyyy'
        :return: dict containing award data

        >>> get_awards_from('12/25/2018')

        """
        self.params['dateStart'] = start_date

        request_url = self.nsf_api + self._build_field_request() + self._build_param_request()

        xml_files = self._send_request_xml(request_url)
        data = self._construct_data_xml(xml_files)

        return data

    def keyword_search(self, *args):
        """
        Take list of keywords to search nsf awards database.

        Returns dictionary of results.

        To match all the words in the phrase, use double quotes
        in the value
        (ex. keyword_search(['nano', '"Pillar Compression"', 'afm']))

            get_keywords_data('keywords-1', 'keyword-2',
                                abstractText=False)

                return data_dictionary
        """
        keywords = args
        request_url = self._assemble_kw_url(keywords)
        # print(request_url)

        xml_files = self._send_request_xml(request_url)
        data = self._construct_data_xml(xml_files)

        return data

    def id_search(self, award_id):
        """
        Perform Search on award ID.

        Take award_id and returns a dictionary containing information on
        that award using the parameter and field dictionaries

            id_search(award_id):
                return dict
        """
        request_url = self._assemble_id_url(award_id)
        xml_files = self._send_request_xml(request_url)
        data = self._construct_data_xml(xml_files)

        return data

    def _assemble_id_url(self, award_id):
        """
        Build ID search URL.

        Take award_id and returnds a request urllib using fields and
        params settings

            _assemble_id_url(award_id)
                return string
        """
        award_id_api = 'http://api.nsf.gov/services/v1/awards/{}.xml?'\
            .format(award_id)
        search_params = self._build_param_request()
        include = self._build_field_request()
        request_url = award_id_api + include + search_params
        return request_url

    def _assemble_kw_url(self, keywords):
        """
        Build keward search URL.

        Takes list of keywords  returns a request urllib using fields
        param settings

            assemble_url(param_dict)
                return('request_url')
        """
        search_params = self._build_param_request()
        include = self._build_field_request()

        keywords = '+'.join(keywords)
        request_url = \
            self.nsf_api + 'keyword=' + keywords + include + search_params

        return request_url

    def _build_param_request(self):
        """
        Build url section for search parameters.

        returns string.

            _build_param_request()
                returns string
        """
        search_params = []
        for param in self.params:
            # print(param)
            if self.params[param] is not None:
                search_params.append(param + '={}'.format(self.params[param]))
        search_params = '&' + '&'.join(search_params)
        return search_params

    def _build_field_request(self):
        """
        Build url section for requesting fields.

        Returns string.

                _build_field_request()
                    returns string
        """
        include = []
        for field in self.fields:
            if self.fields[field] is True:
                include.append(field)
        include = '&printFields=' + ','.join(include)
        return include

    def _send_request_xml(self, request_url):
        """
        Send request to NSF Database.

        Returns xml file object.

            _send_request_xml('request_url')
                return xml_file_obj
        """
        xml_files = []
        page_count = 1

        if page_count == 1:
            r = requests.get(request_url)
            # turns string into file object for passing to ET.parse()
            #print(request_url)
            #print(r.text)
            xml_file = io.StringIO(r.text)
            xml_files.append(xml_file)

        tree = ET.parse(xml_file)
        root = tree.getroot()
        print('\rcollecting page: {} | Entries Found: {}'
              .format(page_count, len(root)), end='')  # -1

        page_count += 1
        if len(root) == 25:
            while len(root) % 25 == 0 and len(root) > 0:
                # print(request_url + '&offset={}'.format(page_count))
                r = requests.get(request_url + '&offset={}'.format(page_count))
                xml_file = io.StringIO(r.text)
                xml_files.append(xml_file)
                tree = ET.parse(xml_file)
                root = tree.getroot()
                xml_file.seek(0)
                # print('end of loop')
                print('\rcollecting page: {} | Entries Found: {}'
                      .format(page_count, len(root)), end='')
                page_count += 1
        print('\n')
        return xml_files

    def _construct_data_xml(self, xml_file_list):
        """
        Parse list of .xml data file objects using xml.eTree.ElementTreeself.

        Returns dictionary of values.

            _construct_data_xml(xml_file_list)
                returns dictionary
        """
        award_dict = {}
        for xml_file in xml_file_list:
            xml_file.seek(0)
            tree = ET.parse(xml_file)
            root = tree.getroot()
            for response in root:
                for award in response:
                    try:
                        award_dict[award.tag].append(award.text)
                    except KeyError:
                        award_dict[award.tag] = [award.text]

            if 'entry' in award_dict.keys():
                del award_dict['entry']

        return award_dict

    def reset(self):
        """
        Reset the fields and params dictionary back to default.

            reset_fields()
                return None
        """
        self.__init__()

    def set_fields(self, **kwargs):
        """
        Set Search Fields.

        Take boolean Keyword arguments for fields to be retrieved during
        the search.

            sef_fields(abstractText=True)
                return

        visit
        https://www.research.gov/common/webapi/awardapisearch-v1.htm
        for detailed discription of search fields.
        """
        for key, value in kwargs.items():
            if key in self.fields.keys():
                if type(value) != bool:
                    raise TypeError('Expecting Bool passed {}'
                                    .format(type(value)))
                self.fields[key] = value
            else:
                raise KeyError

    def set_params(self, **kwargs):
        """
        Take Keyword arguments for search parameters being used.

            set_params(dateStart='01/01/2017',
                        dateEnd='12/31/2017',
                        awardeeStateCode='WI')

        visit
        https://www.research.gov/common/webapi/awardapisearch-v1.htm
        for better discription of search parameters.
        """
        for key, value in kwargs.items():
            if key in self.params.keys():
                self.params[key] = value
            else:
                raise KeyError

    def get_fields(self):
        """Return search fields dictionary."""
        return self.fields

    def get_params(self):
        """Return search parameter dictionary."""
        return self.params

        """
        ____________________________________________________________________________

        Fields retrieved from search by default
        ---------------------------------------
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

        Other retrievable fields
        ------------------------
                'offset' : False
                'awardeeCountryCode' : False,
                'awardeeCounty' : False,
                'awardeeDistrictCode' : False,
                'awardeeZipCode' : False,
                'cfdaNumber' : False,
                'coPDPI' : False,
                'startDate' : False,
                'expDate' : False,
                'estimatedTotalAmt' : False,
                'fundsObligatedAmt' : True,
                'dunsNumber' : False,
                'fundProgramName' : False,
                'parentDunsNumber' : False,
                'pdPIName' : False,
                'perfCity' : False,
                'perfCountryCode' : False,
                'perfCounty' : False,
                'perfDistrictCode' : False,
                'perfLocation' : False,
                'perfStateCode' : False,
                'perfZipCode' : False,
                'poName' : False,
                'primaryProgram' : False,
                'transType' : False,
                'awardee' : False,
                'poPhone' : False,
                'poEmail' : False,
                'awardeeAddress' : False,
                'perfAddress' : False,
                'publicationResearch' : False,
                'publicationConference' : False,
                'fundAgencyCode' : False,
                'awardAgencyCode' : False,
                'projectOutComesReport' : False,
                'abstractText' : False,
                'piMiddeInitial' : False,
                'piLastName' : True,
                'piPhone' : False,
                'piEmail' : False
                """


if __name__ == '__main__':
    test_url = 'http://api.nsf.gov/services/v1/awards.xml?keyword=hysitron&\
        printFields=id,title,agency,awardeeCity,awardeeName,awardeeStateCode,date,\
        fundsObligatedAmt,piFirstName,piLastName'
    nsf = FundNSF()
    #nsf.set_fields(abstractText=True)
    #nsf.set_params(dateStart='01/01/2018', dateEnd='01/15/2018')
    #data = nsf.keyword_search('nano', '"pillar compression"')
    nsf.fields['abstractText'] = True
    data = nsf.get_awards_from('03/20/2018')
    print(data['Title'][0])

    #award_data = nsf.id_search(data['id'][0])
    #print(award_data['abstractText'])
    print(len(data))
