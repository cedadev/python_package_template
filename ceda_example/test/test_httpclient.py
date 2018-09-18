'''Module description
'''
__author__ = "Philip Kershaw" # Put in your name or id
__date__ = "14 Sep 2018"
__copyright__ = "(C) 2018 Science and Technology Facilities Council"
__license__ = "BSD - see LICENSE file in top-level package directory"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
# system package imports first
import unittest
import os
import logging


# Then imports from this package here if needed
from ceda_example.http_client import HttpClient, HttpClientReadFileError

# Then code - you may want to log unit test output but not normally necessary
log = logging.getLogger(__name__)

THIS_DIR = os.path.dirname(os.path.abspath(__file__))


class HttpClientTestCase(unittest.TestCase):
    """Test functionality for CEDA Example HTTP Client class
    """
    TEST_OUTPUT_FILEPATH = os.path.join(THIS_DIR, 'test_output.html')
    
    def test_no_arg_for_contructor(self):
        # Show that when called with no arguments to the constructor it fails
        with self.assertRaises(TypeError):
            HttpClient()
        
    def test_download_file(self):
        http_client = HttpClient('http://www.ceda.ac.uk/')
        
        try:
            http_client.download_file(self.TEST_OUTPUT_FILEPATH)
            self.assertGreater(os.path.getsize(self.TEST_OUTPUT_FILEPATH), 0,
                               "Download file size is zero")  
        finally:
            os.remove(self.TEST_OUTPUT_FILEPATH)
        
    def test_download_file_for_non_existent_uri(self):
        # Make sure HttpClientReadFileError is raised if a non-200 status
        # is returned
        http_client = HttpClient('http://www.ceda.ac.uk/does-not-exist/')
        
        # Using /dev/null for the output file here because we're not 
        # interested in any output
        with self.assertRaises(HttpClientReadFileError):
            http_client.download_file(os.devnull)

            
# Enable unit test to be called as a script
if __name__ == "__main__":
    unittest.main()