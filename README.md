# FundNSF
Python wrapper for National Science Foundations (NSF) award funding API.
FundNSF is for performing searches on the National Science Foundations
(NSF) awards database through their api.

link: https://www.research.gov/common/webapi/awardapisearch-v1.htm


##Example

from fundNSF import FundNSF
import pandas as pd

nsf = FundNSF()
nsf.set_fields(abstractText=True)
nsf.set_params(dateStart='01/01/2017',
          dateEnd='12/31/2017') # enter date as 'mm/dd/yyyy'
data = nsf.keyword_search('nano') #returns a Dictionary
df = pd.DataFrame(data)
print(df.head())

award_data = nsf.id_search(df['id'][0])
print(award_data['abstractText'])

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

Search Parameters
-----------------

More search parameters can be found at
https://www.research.gov/common/webapi/awardapisearch-v1.htm#request-parameters-notes

'offset': None, #Record offset -> page cfdaNumber
'agency': None, # 'NSF' or 'NASA'
'dateStart': None, # Start date for award date to search (ex. 12/31/2012)
'dateEnd': None, #End date for award date to search mm/dd/yyyy
'startDateStart': None, #Start date for award start date to search
'startDateEnd' : None, #End date for award start date to search
'expDateStart' : None, #start date for award exp date to search
'expDateEnd' : None, #end date for award exp date to search
'estimatedTotalAmtFrom' : None,
'estimatedTotalAmtTo' : None,
'estimatedObligatedAmtFrom' : None,
'estimatedObligatedAmtTo' : None,
'awardeeStateCode' : None,
'awardeeName' : None

  Methods defined here:
------------------------

  __init__(self)
      Initialize self.  See help(type(self)) for accurate signature.

  assemble_id_url(self, award_id)
      Takes award_id and returnds a request urllib using fields and
      params settings

          assemble_id_url(award_id)
              return string

  assemble_kw_url(self, keywords)
      Takes list of keywords and returns a request urllib using fields
      param settings

          assemble_url(param_dict)
              return('request_url')

  build_field_request(self)
      builds url section for requesting Fields

              build_field_request()
                  returns string

  build_param_request(self)
      builds url section for search parameters

          build_param_request()
              returns string

  construct_data_xml(self, xml_file_list)
      Parses list of .xml data file objects using xml.eTree.ElementTree
      package returns dictionary of values.

          construct_data_xml(xml_file_list)
              returns dictionary

  get_fields(self)
      returns search fields dictionary

  get_params(self)
      returns search parameter dictionary

  id_search(self, award_id)
      Takes award_id and returns a dictionary containing information on
      that award using the parameter and field dictionaries

          id_search(award_id):
              return dict

  keyword_search(self, *args)
      takes list of keywords to search nsf awards database for

          get_keywords_data(['keywords'],
                              abstractText=False)

              return data_dictionary

  reset(self)
      Resets the fields and params dictionary back to default

          reset_fields()
              return None

  send_request_xml(self, request_url)
      sends request to NSF Database and returns xml file object

          send_request('request_url')
              return xml_file_obj

  set_fields(self, **kwargs)
      Takes boolean Keyword arguments for fields to be retrieved during the
      search

          sef_fields(abstractText=True)
              return

      visit
      https://www.research.gov/common/webapi/awardapisearch-v1.htm
      for detailed discription of search fields

  set_params(self, **kwargs)
      Takes Keyword arguments for search parameters being used

          set_params(dateStart='01/01/2017',
                      dateEnd='12/31/2017',
                      awardeeStateCode='WI')

      visit
      https://www.research.gov/common/webapi/awardapisearch-v1.htm
      for better discription of search parameters
