"""Test Module for fundNSF package."""
from fundNSF import FundNSF

# Create FundNSF() object

nsf = FundNSF()
test_files = []




def test_assemble_id_url():
    """Test _assemble_id_url() Method."""
    id = 1757936
    result = nsf._assemble_id_url(str(id))
    assert result == 'http://api.nsf.gov/services/v1/awards/' + \
        str(id) + \
        '.xml?&printFields=id,agency,awardeeCity,awardeeName,' + \
        'awardeeStateCode,date,fundsObligatedAmt,title,piFirstName,piLastName&'
    assert type(result) is str
    assert str(id) in result


def test_assemble_kw_url():
    """Test _assemble_kw_url() Method."""
    keyword = 'keywords'
    result = nsf._assemble_kw_url([keyword])
    assert result == 'http://api.nsf.gov/services/v1/awards.xml?keyword=' + \
        'keywords&printFields=id,agency,awardeeCity,awardeeName,' + \
        'awardeeStateCode,date,fundsObligatedAmt,title,piFirstName,piLastName&'
    assert type(result) is str
    assert keyword in result

def test_get_award_from():
    """
    Test get_award_from():
    :return:
    """
    nsf.params['dateEnd'] = '05/10/2019'
    result = nsf.get_awards_from('05/10/2019')
    assert len(result) > 1

def test_id_search():
    """Test Assemble_id_url() Method."""
    id = 1757936
    result = nsf.id_search(id)
    assert result is not None
    assert result['title'][0] == 'REU Site: Creative Approaches to ' +\
        'Materials Design and Processing'


def test_keyword_search():
    """Test keyword_search() Method."""
    # Set up small search.
    nsf.set_params(dateStart='01/01/2018', dateEnd='01/15/2018')
    data = nsf.keyword_search('nano', 'pillar')
    assert len(data['title']) == 9  # Number of awards returned
    nsf.reset()


def test_send_request_xml():
    """Test _send_request_xml() Method."""    # Set up small search.
    url = 'http://api.nsf.gov/services/v1/awards/' + \
        str(id) + \
        '.xml?&printFields=id,agency,awardeeCity,awardeeName,' + \
        'awardeeStateCode,date,fundsObligatedAmt,title,piFirstName,piLastName&'
    test_files = nsf._send_request_xml(url)
    assert len(test_files) >= 1
    assert test_files is not None
    assert isinstance(test_files, list)


def test_construct_data_xml():
    """Test _construct_data_xml() Method."""
    url = 'http://api.nsf.gov/services/v1/awards/' + \
        str(id) + \
        '.xml?&printFields=id,agency,awardeeCity,awardeeName,' + \
        'awardeeStateCode,date,fundsObligatedAmt,title,piFirstName,piLastName&'
    test_files = nsf._send_request_xml(url)
    award = nsf._construct_data_xml(test_files)
    assert len(award) >= 1
    assert isinstance(award, dict)


def test_build_field_request():
    """Test _build_field_request() Method."""
    return_list = nsf. _build_field_request()
    assert isinstance(return_list, str)
    assert len(return_list) >= 1
    assert 'id' in return_list


def test_get_fields():
    """Test get_fields() Method."""
    fields = nsf.get_fields()
    assert isinstance(fields, dict)
    assert len(fields) > 1
    assert 'id' in fields


def test_set_fields():
    """Test set_fields() Method."""
    fields = nsf.get_fields()
    assert fields['agency'] is True
    nsf.set_fields(agency=False)
    assert fields['agency'] is False


def test_get_params():
    """Test get_params() Method."""
    params = nsf.get_params()
    assert isinstance(params, dict)
    assert len(params) > 1
    assert 'dateStart' in params


def test_reset():
    """Test reset() Method."""
    nsf.set_fields(agency=False)
    nsf.reset()
    fields = nsf.get_fields()
    assert fields['agency'] is True
