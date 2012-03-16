"""
This script runs the conformance tests to validate the implementation.
"""
import os.path, tempfile
from arelle.tests import TestCntlr, check_and_setup, make_checker

def efm_test():
    dirpath=tempfile.gettempdir()
    short_name = "efm-18-120228.zip"
    url = "http://www.sec.gov/info/edgar/ednews/efmtest/efm-18-120228.zip"
    index = "efm-18-120228/conf/testcases.xml"
    file_name = os.path.join(dirpath, short_name)
    check_and_setup(file_name, url, dirpath, short_name)
    for index, test, variation in TestCntlr().run(os.path.join(dirpath, index), True, True, False):
        yield(make_checker("EFM", test, variation))
