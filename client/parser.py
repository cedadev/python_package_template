#!/usr/bin/env python

"""
CMMSParser.py
======================

A parsing script to read in YAML files from the CEDA Manual Metadata Store (CMMS).

It will :
 - check that the requested YAML file exists in the CMMS, else return empty response
 - If it exists it will read in the contents and check for valid YAML
 - then test each item to make sure that it conforms to the requirements for each CMMS field
 
 
python cmms_parser.py <uuid>

 
Written by: G A Parton

Creation: 01 Oct 2018

Version 1.0: initial scripting


"""
__author__ = "Graham Parton"
__date__ = "17 Oct 2018"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"
__contact__ = "graham.parton@stfc.ac.uk"
__all__ = ['CMMSParser']

# first let's call in the standard libraries typically needed when interacting with MOLES stuff...

import datetime
import yaml
import requests
import re
from yamllint.config import YamlLintConfig
from yamllint import linter
yamllin_conf = YamlLintConfig('extends: default')



class CMMSParser(object):
    '''
    check for existance of CEDA YAML file for the submitted uuid
    :param
    '''


    def __init__(self, uuid, test=False):


        self.uuid = uuid
        self.cmms_url = 'https://raw.githubusercontent.com/cedadev/cmms/master/yaml_files/%s.yml'

        if test and self.uuid[0:4] in ['geo_','bad_']:
            self.cmms_url = 'https://raw.githubusercontent.com/cedadev/cmms/master/test_yaml/%s.yml'
        if 'full_example' in uuid:
            self.cmms_url = 'https://raw.githubusercontent.com/cedadev/cmms/master/example_yaml/%s.yml'
        self.field_mappings = {'splice rules': 'splice rules',
                               'phenomena': 'phenomena',
                               'time_range': 'temporalRange',
                               'bbox': 'geographicExtent',
                               'n_files': 'numberOfFiles',
                               'size': 'volume',
                               'format': 'fileFormat',
                               'accessType': 'accessType',
                               'accessRoles': 'accessRoles',
                               'licenceUrl': 'licenceUrl',
                               'lastUpdate': 'lastUpdate'}

        self.yaml_content = {}
        self.content = {}
        self.errors = {}
        self._check_and_get_yaml()
        self._parse_yaml_content()

    def _check_and_get_yaml(self):
        '''
        attemots
        :param self:
        :return: self.errors with error information as required OR self.content with read in yaml_content
        '''
        ret = requests.get(self.cmms_url% self.uuid)

        if ret.status_code == requests.codes.ok:
            try:
                self.yaml_content = yaml.load(ret.text)
                gen = linter.run(ret.text, yamllin_conf)
                lint_errors = list(gen)
                if lint_errors:
                    for lint_error in lint_errors:
                        if 'duplication of key' in lint_error.message:
                            self.errors['yamllint'] = lint_error
                            dup_key = re.search('duplication of key "(?P<key>\w{1,})"',lint_error.message).groupdict()['key']
                            del self.yaml_content[dup_key]


            except yaml.YAMLError as e :
                self.errors['yaml_check'] = e
        elif ret.status_code == 404:
            self.errors['cmms_check'] = 'no CMMS entry for %s'% self.uuid
        else:
            self.errors['cmms_check'] = 'CMMS retrieval error: %s' % ret.status_code


    def _parse_yaml_content(self):
        '''
        will work through the self.yaml_content dictionary
        to check the content and places passed content into self.content

        :param self:
        :return: self.content
        '''

        for yaml_field in self.yaml_content:
            if self.field_mappings.has_key(yaml_field):
                yaml_check = '_check_and_parse_' + yaml_field.replace(' ','_')
                getattr(self,yaml_check)()
            else:
                self.errors['field_check'] = 'the field "%s" is not a permitted CMMS field'% yaml_field

    def _check_and_parse_splice_rules(self):
        '''
        check each splice rule that is given in the file, checking:
            1) is it a valid field name or the 'default' option
            2) that there is an associated field that it applies to in the file
            3) that the rule is from the permitted options

        :return:
        '''
        splice_options = ['default',
                          'cmms_only',
                          'replace',
                          'append',
                          'replace_append',
                          'append_new_only']
        splice_error_msg = ''
        for splice_item_name, splice_rule in self.yaml_content['splice rules'].items():
            if splice_item_name.lower() in self.field_mappings.keys() + ['default']:
                if self.yaml_content.has_key(splice_item_name):
                    if splice_rule in splice_options:
                        if self.content.has_key(self.field_mappings['splice rules']):
                            self.content[self.field_mappings['splice rules']][splice_item_name] = splice_rule
                        else:
                            self.content[self.field_mappings['splice rules']] = {splice_item_name : splice_rule}
                    else:
                        splice_error_msg = '"%s" is not a permitted splice rule option'% splice_rule

                else:
                    splice_error_msg = '"%s" splice rule exists, but no content in yaml file, so not made available'% splice_item_name

            else:
                splice_error_msg = '"%s" is not a recognised CMMS field name'% splice_item_name

            if splice_error_msg:
                if self.errors.has_key('splice_rules'):
                    self.errors['splice_rules'].append(splice_error_msg)
                else:
                    self.errors['splice_rules'] = [splice_error_msg]


    def _check_and_parse_phenomena(self):
        if isinstance(self.yaml_content['phenomena'], (str,list)):
            self.content[self.field_mappings['phenomena']] = self.yaml_content['phenomena']
        else:
            self.errors['phenomena'] = 'phenomena needs to be either just one string or a list of entries (which can be strings or dictionaries)'

    def _check_and_parse_time_range(self):
        date_bits = {}
        try:
            if isinstance(self.yaml_content['time_range']['start'], datetime.date):
                self.yaml_content['time_range']['start'] = datetime.datetime.combine(self.yaml_content['time_range']['start'], datetime.time(0,0))
            if isinstance(self.yaml_content['time_range']['start'], datetime.datetime):
                date_bits['startTime'] = self.yaml_content['time_range']['start']

                if self.yaml_content['time_range'].has_key('end'):
                    if isinstance(self.yaml_content['time_range']['end'], datetime.date):
                        self.yaml_content['time_range']['end'] = datetime.datetime.combine(
                            self.yaml_content['time_range']['end'], datetime.time(23, 59, 59))

                    if isinstance(self.yaml_content['time_range']['end'],datetime.datetime):
                        if self.yaml_content['time_range']['end'] > self.yaml_content['time_range']['start'] :
                            date_bits['endTime'] = self.yaml_content['time_range']['end']
                        else:
                            self.errors['time_range'] = 'end time preceeds start time!'
                    else:
                        self.errors['time_range'] = 'end time is not in yyyy-mm-dd hh:mm:ss format. No date info supplied.'
                        # as the end date isn't set properly it's best not to supply any date info
                        date_bits = {}
                if date_bits:
                    self.content[self.field_mappings['time_range']] = date_bits

            else:
                self.errors['time_range'] = 'start time is not in yyyy-mm-dd hh:mm:ss format'

        except ValueError as e:
            self.errors['time_range'] = '%s'% e

    def _check_and_parse_bbox(self):
        if self.yaml_content['bbox']['east'] <= 180 and self.yaml_content['bbox']['west'] >= -180:
            if self.yaml_content['bbox']['east'] >= self.yaml_content['bbox']['west'] and self.yaml_content['bbox']['north'] >= self.yaml_content['bbox']['south']:

                self.content[self.field_mappings['bbox']] = {'northBoundLatitude' : self.yaml_content['bbox']['north'],
                                                            'eastBoundLongitude' : self.yaml_content['bbox']['east'],
                                                            'westBoundLongitude' : self.yaml_content['bbox']['west'],
                                                            'southBoundLatitude' : self.yaml_content['bbox']['south']}
            else:
                self.errors['bbox'] = 'north and east values must be same or greater than south and west values'
        else:
            self.errors['bbox'] = 'longitude not on -180 to + 180 grid'

    def _isFloat(self, value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def _check_and_parse_size(self):

        size_mappings = {'b' : 0,
                         'kb' : 1,
                         'mb' : 2,
                         'gb' : 3,
                         'tb' : 4,
                         'pb' : 5}



        if isinstance(self.yaml_content['size'], str):
            size_details = self.yaml_content['size'].split(' ')
            amount = size_details[0].strip()
            unit = size_details[1].strip().lower()

        else:
            amount = self.yaml_content['size']
            unit = 'b'


        if self._isFloat(amount):

            if unit in size_mappings:
                self.content[self.field_mappings['size']] = float(amount) * 1024 ** size_mappings[unit]
            else:
                self.errors['size'] = '"%s" not a valid unit' % unit

        else:
            self.errors['size'] = '"%s" is not a valid number'% amount


    def _check_and_parse_n_files(self):
        if isinstance(self.yaml_content['n_files'], int):
            self.content[self.field_mappings['n_files']] = self.yaml_content['n_files']
        else:
            self.errors['n_files'] = 'given value is not an integer'

    def _check_and_parse_accessType(self):
        access_types = ['public', 'registered', 'restricted']
        access_option = self.yaml_content['accessType']

        if access_option in access_types:

            if access_option == 'restricted':

                if self.yaml_content.has_key('accessRoles'):
                    self._check_and_parse_accessRoles()
                    if self.content.has_key('accessRoles'):
                        self.content['accessType'] = self.yaml_content['accessType'] # To do: some code is needed here!!!

                else:
                    self.errors['accessType'] = 'access roles are missing - required for accessType = restricted'

            elif not self.yaml_content.has_key('accessRoles'):
                self.content[self.field_mappings['accessType']] = self.yaml_content['accessType']

            else:
                self.errors['acesssType'] = 'access roles provided, but not consistent with access types selected' \
                                            ' "%s" '% self.yaml_content['accessType']
        else:
            self.errors['accessType'] = '"%s" is not a permitted option'% access_option

    def _check_and_parse_accessRoles(self):
        if isinstance(self.yaml_content['accessRoles'], (str, list)):
            self.content[self.field_mappings['accessRoles']] = self.yaml_content['accessRoles']
        else:
            self.errors['accessRoles'] = 'access roles need to be a string or list object'

    def _check_and_parse_licenceUrl(self):
        try:
            ret = requests.get(self.yaml_content['licenceUrl'])

        except requests.RequestException as e:
            self.errors['licenceUrl'] = 'error on checking licenceUrl: %s'% e

        else:
            if ret.status_code == requests.codes.ok:
                self.content[self.field_mappings['licenceUrl']] = self.yaml_content['licenceUrl']
            elif ret.status_code == 404:
                self.errors['licenceUrl'] = 'invalid URL for licenceUrl field'
            else:
                self.errors['licenceUrl'] = 'licence retrieval error: %s' % ret.status_code
