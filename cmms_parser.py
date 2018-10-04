#!/usr/bin/env python

"""
cmms_parser.py
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
# first let's call in the standard libraries typically needed when interacting with MOLES stuff...

import re
import calendar
import datetime
import codecs
#from ruamel import yaml
import yaml
import collections
import requests
import json

uuids = ['455f0dd48613dada7bfb0ccfcb7a7d41','220a65615218d5c9cc9e4785a3234bd0'] #midas collection - no CMMS entry


cmms_url = 'https://raw.githubusercontent.com/cedadev/cmms/master/yaml_files/%s.yml'

def read_in_cmms(uuid):
    '''
    function to read in yaml file
    '''
    import urllib
    txt = urllib.urlopen(target_url).read()

def cmms_entry_exists(uuid):
    '''
    check for existance of CEDA YAML file for the submitted uuid
    '''
    ret = requests.get(cmms_url% uuid)
    if ret.status_code == requests.codes.ok:
        stuff  = yaml.load(ret.text)
        print yaml.dump(stuff)
    else:
        print 'not in CMMS>', ret.status_code    
    import pdb;pdb.set_trace()


for uuid in uuids:
    apple = cmms_entry_exists(uuid)

'''
for uuid, phenoms_list in fbi_obs_to_phenoms.items():
    with open(os.path.join(output_dir, '%s.yml'% uuid), 'w') as outfile:
        
        #yaml_contents = {'splice rules': {'phenomena' : 'cmms_only'}}
        yaml_contents = {'splice rules' : {'phenomena' : 'append_new_only'}}
        
        #yaml_contents.update(phenoms_list)
        
        #for yaml_content in yaml_contents.items():
        yaml.dump(yaml_contents, outfile, default_flow_style=False)#, Dumper=ruamel.yaml.RoundTripDumper)
        yaml.dump(phenoms_list, outfile, default_flow_style=False)#, Dumper=ruamel.yaml.RoundTripDumper)

s'''
