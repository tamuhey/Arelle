"""
This script runs the conformance tests to validate the implementation.
"""
import os.path, tempfile
from arelle.tests import TestCntlr, check_and_setup, make_checker

def xbrl_test():
    dirpath=tempfile.gettempdir()
    short_name = "XBRL-CONF-CR4-2008-07-02.zip"
    url = "http://www.xbrl.org/2008/XBRL-CONF-CR4-2008-07-02.zip"
    svn_repo = "http://publicsvn.xbrl.org/svn/public/base-specification-conformance/2008-07-02/"
    index = "XBRL-CONF-CR4-2008-07-02/xbrl.xml"
    file_name = os.path.join(dirpath, short_name)
    check_and_setup(file_name, url, dirpath, short_name)
    for index, test, variation in TestCntlr().run(os.path.join(dirpath, index), False, False, True):
        yield(make_checker("XBRL", test, variation))
            