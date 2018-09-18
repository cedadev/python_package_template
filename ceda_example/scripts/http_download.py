# encoding: utf-8
'''ceda_example.scripts.http_download
'''
__author__ = "Philip Kershaw" 
__date__ = "17 Sep 2018"
__copyright__ = "(C) 2018 organization_name"
__license__ = "license"
__contact__ = "Philip.Kershaw@stfc.ac.uk"
__all__ = ['HttpDownloadCLI']
import logging
from argparse import ArgumentParser

from ceda_example import __version__
from ceda_example.http_client import HttpClient

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)


class HttpDownloadCLI:
    """HTTP Download script
    """

    @classmethod
    def main(cls, *argv):
        """Command line options.
        """

        # Setup argument parser
        parser = ArgumentParser(description='HTTP Download client')

        program_version_message = '{} v{}'.format(parser.prog, __version__)
        
        parser.add_argument("-d", "--debug", action="store_true", 
                            dest="debug", default=False,
                            help="Print debug information.")
        
        parser.add_argument('-V', '--version', action='version', 
                            version=program_version_message)

        parser.add_argument("-u", "--uri",  
                            dest="uri", help="Download location.")

        parser.add_argument("-o", "--output-file", 
                            dest="output_filepath",
                            help="file path for output.")
          
        # Parses from arguments input to this method if set, otherwise parses
        # from sys.argv
        if len(argv) > 0:
            parsed_args = parser.parse_args(argv)
        else:
            parsed_args = parser.parse_args()

        if parsed_args.debug:
            logging.getLogger().setLevel(logging.DEBUG)    

        # Need both download URL and destination file
        if parsed_args.uri and parsed_args.output_filepath:
            client = HttpClient(parsed_args.uri)
            client.download_file(parsed_args.output_filepath)
        else:
            log.debug("Both URI and download destination options are needed")
            parser.print_help()
            raise SystemExit(1)
        
        
if __name__ == "__main__":
    HttpDownloadCLI.main()

        
