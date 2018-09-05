# FundNSF
---
Python 3 wrapper for National Science Foundations (NSF) award funding API.
fundNSF is for performing searches on the National Science Foundations
(NSF) awards database through their api.


[PyPi](https://pypi.org/project/fundNSF/)

[![PyPI version](https://badge.fury.io/py/fundNSF.svg)](https://badge.fury.io/py/fundNSF)

[Github](https://github.com/C-NoBlok/fundNSF)

[NSF API Website](https://www.research.gov/common/webapi/awardapisearch-v1.htm)

## Installation

installation through pip is recommended:

    pip install fundNSF

## Example

```python
from fundNSF import FundNSF

nsf = FundNSF()
nsf.set_fields(abstractText=True)
nsf.set_params(dateStart='01/01/2018', dateEnd='01/31/2018') # enter date as 'mm/dd/yyyy'
data = nsf.keyword_search('nano') #returns a Dictionary
print(data['title'][0])

CAREER:Active Nano-Acoustic Waveguide Matrix to Tackle Signal
Processing Limits: Enabling Wideband and Nonreciprocal Integrated
Communication Beyond the UHF

award_data = nsf.id_search(data['id'][0])
print(award_data['fundsObligatedAmt'][0])

500000
```
### Used below fields as keywords in set_fields() method to set the fields being retireved.  
##### Fields retrieved from search by default
```
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
```

##### Other retrievable fields
```
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
```


### Search Parameters
Use as keywords in set_params() method to set search criteria.
More search parameters can be found at the [NSF API Website](https://www.research.gov/common/webapi/awardapisearch-v1.htm#request-parameters-notes).

```
'offset': None,               #Record offset -> page cfdaNumber
'agency': None,               #'NSF' or 'NASA'
'dateStart': None,            #Start date for award date to search (ex. 12/31/2012)
'dateEnd': None,              #End date for award date to search mm/dd/yyyy
'startDateStart': None,       #Start date for award start date to search
'startDateEnd' : None,        #End date for award start date to search
'expDateStart' : None,        #start date for award exp date to search
'expDateEnd' : None,          #end date for award exp date to search
'estimatedTotalAmtFrom' : None,
'estimatedTotalAmtTo' : None,
'estimatedObligatedAmtFrom' : None,
'estimatedObligatedAmtTo' : None,
'awardeeStateCode' : None,
'awardeeName' : None
```


## Methods:


#### keyword_search(*args)
takes list of keywords to search nsf awards database for
```python
get_keywords_data(['keywords'], abstractText=False)
return data_dictionary
```


#### id_search(award_id)
Takes award_id and returns a dictionary containing information on
that award using the parameter and field dictionaries
```python
id_search(award_id):
return dict
```


#### reset()
Resets the fields and params dictionary back to default
```python
reset_fields()
```           


#### set_fields(self, **kwargs)
Takes boolean Keyword arguments for fields to be retrieved during the search

```python
sef_fields(abstractText=True)
```
visit: https://www.research.gov/common/webapi/awardapisearch-v1.htm
for detailed discription of search fields


#### set_params(self, **kwargs)
Takes Keyword arguments for search parameters being used
```python
set_params(dateStart='01/01/2017', dateEnd='12/31/2017', awardeeStateCode='WI')
```
visit the [NSF API Website](https://www.research.gov/common/webapi/awardapisearch-v1.htm#request-parameters-notes) for better discription of search parameters


#### get_fields(self)
returns search fields dictionary


#### get_params(self)
returns search parameter dictionary
