# FundNSF
Python wrapper for National Science Foundations (NSF) award funding API.
FundNSE is for performing searches on the National Science Foundations
(NSF) awards database through their api.

link:
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
