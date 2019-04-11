from cmms.client.parser import CMMSParser
from yaml import YAMLError

def check_err(test_string, err_entry ):
    if isinstance(err_entry, str):
        err_entry = [err_entry]
    for err in err_entry:
        if test_string in err:
            return True
    raise Exception('{} not in {}'.format(test_string, err_entry))

def test_BadSplice_keyIsNotRecognisedCMMSfield_sucess():
    ''
    uuid = 'bad_splice'
    parsed_item = CMMSParser(uuid, test=True)
    check_err('is not a recognised CMMS field name', parsed_item.errors['splice_rules'])


def test_BadSplice_RuleNotPermittedOption_sucess():
    'splice option is not from permitted list'
    uuid = 'bad_splice_rule'
    parsed_item = CMMSParser(uuid, test=True)
    check_err('is not a permitted splice rule option', parsed_item.errors['splice_rules'])


def test_BadSplice_SpliceRuleOKButNoMatchingFieldinYAML_sucess():
    'Splice rule is fine, but the YAML file is missing the corresponding CMMS field'
    uuid = 'bad_splice_no_match'
    parsed_item = CMMSParser(uuid, test=True)
    check_err('splice rule exists, but no content in yaml file, so not made available', parsed_item.errors['splice_rules'])


def test_BadYAML():
    'YAML just does not parse'
    uuid = 'bad_yaml_format'
    parsed_item = CMMSParser(uuid, test=True)
    assert(isinstance(parsed_item.errors['yaml_check'], YAMLError))


def test_BadSplice_DuplicateField_sucess():
    'has one of the fields repeated, so field is stripped out'
    uuid = 'bad_duplicate_field'
    parsed_item = CMMSParser(uuid, test=True)
    assert('duplication of key' in parsed_item.errors['yamllint'].desc)


def test_BadAccessType_success():
    'item is not from the permitted list'
    uuid = 'bad_access'
    parsed_item = CMMSParser(uuid, test=True)
    check_err('is not a permitted option', parsed_item.errors['accessType'])


def test_BadLicenceURL_success():
    'not valid url - either not a http url or 404 error'
    uuid = 'bad_licence'
    parsed_item = CMMSParser(uuid, test=True)
    check_err('error on checking licenceUrl:', parsed_item.errors['licenceUrl'])


def test_BadParameterEntries_success():
    '(list) badly formed (not list? or dictionary items not dictionary items)'
    uuid = 'bad_params'
    parsed_item = CMMSParser(uuid, test=True)
    check_err('phenomena needs to be either just one string or a list of entries', parsed_item.errors['phenomena'])


def test_BadSize_unitsNotRecognised_success():
    'units are not from a prescribed list'
    uuid = 'bad_size'
    parsed_item = CMMSParser(uuid, test=True)
    check_err('not a valid unit', parsed_item.errors['size'])


def test_BadSize_checkingIfItCanCopeWithExponentialValue_success():
    'checking that exponential values are handled OK'
    uuid = 'bad_size_expo'
    parsed_item = CMMSParser(uuid, test=True)
    assert(parsed_item.content['volume'] == 31457280000.0)


def test_BadSize_typoInNumber_success():
    'value has a typo in it - i.e. not a number'
    uuid = 'bad_size_typo'
    parsed_item = CMMSParser(uuid, test=True)
    check_err('is not a valid number', parsed_item.errors['size'])


def test_BadTemporal_notAValidDate_success():
    'date is not in ISO format'
    uuid = 'bad_temp'
    parsed_item = CMMSParser(uuid, test=True)
    check_err('start time is not in yyyy-mm-dd hh:mm:ss format', parsed_item.errors['time_range'])


def test_BadTemporal_notFullISODateTime_success():
    'not in full yyyy-mm-dd hh:mm:ss format'
    uuid = 'bad_temp_format'
    parsed_item = CMMSParser(uuid, test=True)
    check_err('end time is not in yyyy-mm-dd', parsed_item.errors['time_range'])


def test_BadTemp_endTimeBeforeStart_success():
    'checks that start time <= end_time'
    uuid = 'bad_temp_backwards'
    parsed_item = CMMSParser(uuid, test=True)
    check_err('end time preceeds', parsed_item.errors['time_range'])


def test_BadGeo_gridValuesFlipped_success():
    'lat, lon are wrong way around (i.e. southen bound is higher lat than n. bound)'
    uuid = 'geo_flipped'
    parsed_item = CMMSParser(uuid, test=True)
    check_err('north and east values must be same or greater than south and west values', parsed_item.errors['bbox'])


def test_BadGeo_notOn180Grid_success():
    'lat is outside -180 -> 180 range'
    uuid = 'geo_not_180'
    parsed_item = CMMSParser(uuid, test=True)
    check_err('longitude not on -180 to + 180 grid', parsed_item.errors['bbox'])


def test_BadFileNum_notIntValue_success():
    'number of files is not an integer'
    uuid = 'bad_num'
    parsed_item = CMMSParser(uuid, test=True)
    check_err('given value is not an integer', parsed_item.errors['n_files'])


def test_MIDASDataset_successful_parsing():
    ''
    uuid = '455f0dd48613dada7bfb0ccfcb7a7d41'
    parsed_item = CMMSParser(uuid, test=True)
    assert(not parsed_item.errors)


def test_MIDASCollection_noYAMLFound_success():
    ''
    uuid = '220a65615218d5c9cc9e4785a3234bd0'
    parsed_item = CMMSParser(uuid, test=True)
    check_err('no CMMS entry for', parsed_item.errors['cmms_check'])



def test_FullExampleYAML_test_success():
    ''
    uuid = 'full_example'
    parsed_item = CMMSParser(uuid, test=True)
    assert(not parsed_item.errors)

def test_FullExampleYAML_success():
    ''
    uuid = 'full_example'
    parsed_item = CMMSParser(uuid)
    assert(not parsed_item.errors)
'''
uuids = ['455f0dd48613dada7bfb0ccfcb7a7d41','220a65615218d5c9cc9e4785a3234bd0'] #midas collection - no CMMS entry


'''