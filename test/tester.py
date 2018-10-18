from CMMSParser import CMMSParser

test = True


uuids = ['455f0dd48613dada7bfb0ccfcb7a7d41','220a65615218d5c9cc9e4785a3234bd0'] #midas collection - no CMMS entry
test_uuids =   ['bad_splice', # splice rule field isn't from permitted field list
                'bad_splice_rule', # given rule isn't from permitted list
                'bad_splice_no_match', # rule exists, but no associated field
                'bad_yaml_format',
                'bad_duplicate_field', # has one of the fields repeated - expect that it'll just do one
                'bad_access', # 0..1 not from controlled list (typo)
                'bad_licence', # 0..1 not valid url - either not a http url or 404 error
                'bad_params', # 0.. 1 (list) badly formed (not list? or dictionary items not dictionary items)
                'bad_size', # not number with recognsied units
                'bad_size_expo', # checking to see how exponential values are handled
                'bad_size_typo', # value has typo in it
                'bad_temp', # string as opposed to a yyyy-mm-dd hh:mm:ss.ss
                'bad_temp_format', # not in full yyyy-mm-dd hh:mm:ss format
                'bad_temp_backwards', #checks that start time <= end_time
                'geo_flipped', # lat, lon are wrong way around (i.e. southen bound is higher lat than n. bound)
                'geo_not_180', # lat is outside -180 -> 180 range
                'bad_num', # number of files isn't an integer
                '455f0dd48613dada7bfb0ccfcb7a7d41',
                '220a65615218d5c9cc9e4785a3234bd0',
                'full_example'
                ]



print 'here'
for uuid in test_uuids:


    print uuid
    apple = CMMSParser.CMMSParser(uuid, test = True)
    print apple.content
    print apple.errors


