"""
This script runs the conformance tests to validate the implementation.
"""
import os.path, tempfile
from arelle.tests import TestCntlr, check_and_setup, make_checker

def xdt_test():
    dirpath=tempfile.gettempdir()
    short_name = "XDT-CONF-CR4-2009-10-06.zip"
    url = "http://www.xbrl.org/2009/XDT-CONF-CR4-2009-10-06.zip"
    index = "XDT-CONF-CR4-2009-10-06/xdt.xml"
    file_name = os.path.join(dirpath, short_name)
    check_and_setup(file_name, url, dirpath, short_name)
    for index, test, variation in TestCntlr().run(os.path.join(dirpath, index), False, False, False): 
        yield(make_checker("XDT", test, variation))
