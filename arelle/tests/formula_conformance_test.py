"""
This script runs the conformance tests to validate the implementation.
"""
import os.path, tempfile
from arelle.tests import TestCntlr, check_and_setup, make_checker

def formula_test():
    dirpath=tempfile.gettempdir()
    short_name = "Formula-CONF-REC-PER-Errata-2011-03-16.zip"
    url = "http://www.xbrl.org/Specification/formula/REC-2009-06-22/conformance/Formula-CONF-REC-PER-Errata-2011-03-16.zip"
    index = "REC-PER-Errata-testcases-2011-03-16/index.xml"
    file_name = os.path.join(dirpath, short_name)
    check_and_setup(file_name, url, dirpath, short_name)
    for index, test, variation in TestCntlr().run(os.path.join(dirpath, index), False, False, False):
        yield(make_checker("Formula", test, variation))
