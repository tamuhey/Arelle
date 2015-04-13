"""
This script runs the conformance tests to validate the implementation.
"""
import os, os.path, gettext, nose, urllib.request, zipfile, logging
from functools import partial
from arelle import Cntlr, FileSource, ModelDocument
from arelle.ModelFormulaObject import FormulaOptions

gettext.install("arelle")
logging.basicConfig(level=logging.DEBUG)

class TestCntlr(Cntlr.Cntlr):
    """The function used to wrap tests."""
    def __init__(self):
        super(TestCntlr, self).__init__()
        self.messages = []
        self.outcomes = list()
        
    def run(self, testfn, ds, utr, dec):
        """The run method is invoked to make things happen."""
        self.messages = []
        filesource = FileSource.FileSource(testfn, self)

        self.modelManager.validateUtr = utr
        if ds:
            self.modelManager.validateDisclosureSystem = True
            self.modelManager.disclosureSystem.select("efm")
        else:
            self.modelManager.disclosureSystem.select(None)
            
        if dec:
            self.modelManager.validateInferDecimals = True
            self.modelManager.validateCalcLB = True

        self.modelManager.formulaOptions = FormulaOptions()

        modelXbrl = self.modelManager.load(filesource, gettext.gettext("validating"))
        self.modelManager.validate()
        modelDocument = modelXbrl.modelDocument

        if modelDocument is not None:
            if modelDocument.type in (ModelDocument.Type.TESTCASESINDEX, ModelDocument.Type.REGISTRY):
                index = os.path.basename(modelDocument.uri)
                for tci in modelDocument.referencesDocument.keys():
                    tc = modelXbrl.modelObject(tci.objectId())
                    test_case = os.path.basename(tc.uri)
                    if hasattr(tc, "testcaseVariations"):
                        for mv in tc.testcaseVariations:
                            self.outcomes.append((index, test_case, mv))
            elif modelDocument.type in (ModelDocument.Type.TESTCASE, ModelDocument.Type.REGISTRYTESTCASE):
                tc = modelDocument
                test_case = os.path.basename(tc.uri)
                if hasattr(tc, "testcaseVariations"):
                    for mv in tc.testcaseVariations:
                        self.outcomes.append((None, test_case, mv))

        return self.outcomes
        
    def addToLog(self, message):
        logging.info(message.rstrip() + '\n')

    def showStatus(self, msg, clearAfter=None):
        pass
    
def check_variation(variation):
    assert variation.status == "pass", "(%s) %s != %s" % (variation.status, variation.expected, variation.actual)
 
def make_checker(name, test, variation):
    tname = os.path.splitext(test)[0]
    z = partial(check_variation, variation)
    z.description = "%s [ %s ] %s %s" % (name, tname, variation.id, variation.name)
    setattr(z, "__module__", "%s %s" % (name, tname))
    setattr(z, "__name__", "%s %s" % (variation.id, variation.name))
    return(z)

def check_and_setup(file_name, url, dirpath, short_name):
    # Check to see if we have zip files, if not download them
    if not os.path.exists(file_name):
        try:
            file_name, hdrs = urllib.request.urlretrieve(url, file_name)
        except IOError as e:
            logging.exception("can't retrieve %r to %r: %s" % (url, file_name, e))
            return

    # Unpack zipfiles each time to ensure the tests are pristine
    zip = zipfile.ZipFile(file_name)
    
    # Check to make sure this unpacks to it's own directory
    if len(set(map(lambda x: x.split(os.sep)[0], zip.namelist()))) > 1:
        zipdir = os.path.join(dirpath, os.path.splitext(short_name)[0])
    else:
        zipdir = dirpath
    try:
        zip.extractall(path=zipdir)
    except:
        logging.exception("Failed to open zipfile for %s (%s)" % (file_name, zipdir))