'''ceda_example.http_client - simple example class for reading HTTP content
'''
__author__ = "Philip Kershaw"
__date__ = "14 Sep 2018"
__copyright__ = "Copyright 2018 United Kingdom Research and Innovation"
__license__ = "BSD - see LICENSE file in top-level package directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__all__ = ['HttpClient']
from http import HTTPStatus # system package imports first
import logging

import requests # then 3rd party package imports

# Then imports from this package here if needed

# Then code
log = logging.getLogger(__name__)


class HttpClientError(Exception):
    """Base class for CEDA Example HTTP Client exceptions"""
    

class HttpClientReadFileError(HttpClientError):
    """Error reading file from given link"""
    
 
# For Python 2, inherit from object so that you can get new-style class
# features.  In Python 3 this is not necessary   
class HttpClient: 
    '''Simple HTTP client class for illustration
    '''
    HTTP_CHUNK_SIZE = 1024
    
    def __init__(self, uri):
        '''Set the URI to operate on
        
        :param uri: URI to operate on
        '''
        self.uri = uri
        
    def download_file(self, output_filepath):
        """HTTP GET a file from a given URI
        
        :param output_filepath: destination location for downloaded output
        """
        log.debug('Getting {!r} and saving to {!r}'.format(self.uri, 
                                                           output_filepath))
        response = requests.get(self.uri)
        
        if response.status_code != HTTPStatus.OK:
            error_msg = ("Error downloading file from {!r}; status code is "
                         "{!r}".format(self.uri, response.status_code))
            log.exception(error_msg)
            raise HttpClientReadFileError(error_msg)
        
        with open(output_filepath, 'wb') as file_out:
            for chunk in response.iter_content(
                                            chunk_size=self.HTTP_CHUNK_SIZE): 
                if chunk:
                    file_out.write(chunk)
        
