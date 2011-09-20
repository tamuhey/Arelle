import io
import logging
import os.path
import tempfile
import shutil
import zipfile
import re
import gettext
import sys
import argparse
import json

gettext.install("arelle")

from arelle.Cntlr import Cntlr
from arelle import FileSource

log = logging.getLogger(__name__)


class StructuredLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.messages = []
        
    def flush(self):
        """ Nothing to Flush """

    def emit(self, logRecord):
        if not logRecord.args or len(logRecord.args) == 0:
            logRecord.args = {}
        if 'error' in logRecord.args and isinstance(logRecord.args['error'], Exception):
            logRecord.args['error'] = repr(logRecord.args['error'])
        data = {"id": logRecord.messageCode + ":" + logRecord.href,
                "levelname": logRecord.levelname,
                "messageCode": logRecord.messageCode,
                "msg": logRecord.msg % logRecord.args,
                "args": logRecord.args,
                "file": logRecord.file,
                "sourceLine": logRecord.sourceLine,
                "href": logRecord.href}
        self.messages.append(data)

class BasicController(Cntlr):

    def showStatus(self, message, clearAfter=None):
        pass

    def addToLog(self, message):
        pass

def primary_archive_file(archive):
        zf = zipfile.ZipFile(archive)
        files = zf.namelist()
        files = [n for n in files if not re.match(".*\/.*", n)]
        files = [n for n in files if not re.match(".*\.xsd$", n)]
        files = [n for n in files if not re.match(".*\_[a-zA-Z]{3}\.xml$", n)]
        files = [n for n in files if not re.match(".*\_dirty\..*", n)]
        assert len(files) == 1
        return files[0]
    

def normalized_file_source(file_or_path):
    if isinstance(file_or_path, FileSource.FileSource):
        return file_or_path

    # File-like object with existing filesystem path
    file_name = getattr(file_or_path, "name", None)
    if isinstance(file_or_path, io.IOBase) and file_name:
        file_source = FileSource.FileSource(file_name)
        file_source.open()
        if zipfile.is_zipfile(file_or_path):
            file_source.select(primary_archive_file(file_or_path))
        return file_source

    # All other readable, file-like objects
    if isinstance(file_or_path, io.IOBase):
        try:
            temp = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
                        
            file_or_path.seek(0)
            shutil.copyfileobj(file_or_path, temp)
            temp.flush()

            file_source = FileSource.FileSource(temp.name)
            file_source.open()
            if zipfile.is_zipfile(temp):
                temp.seek(0)
                file_source.select(primary_archive_file(temp))                        
            return file_source
        except AssertionError:
            return None
    
    if isinstance(file_or_path, str):
        return normalized_file_source(open(file_or_path, "rb"))

    if isinstance(file_or_path, bytes):
        return normalized_file_source(open(file_or_path.decode(), "rb"))

    return None

        
def validate(file_or_path=None, disclosure_system=None, infer_decimals=False, calc_linkbase=False, utr=False, **kwargs):
    gettext.install("arelle")
    log_handler = StructuredLogHandler()
    logging.getLogger("arelle").addHandler(log_handler)

    controller = BasicController()
    manager = controller.modelManager
    if disclosure_system:
        log.info("disclosure_system = %s" % disclosure_system)
        manager.validateDisclosureSystem = True
        manager.disclosureSystem.select(disclosure_system)
    manager.validateInferDecimals = infer_decimals
    manager.validateCalcLB = calc_linkbase
    manager.validateUtr = utr

    try:
        file_source = normalized_file_source(file_or_path)
        log.debug(file_source)
        if file_source:
            manager.load(file_source, "loading file source")
            manager.validate()
        
    finally:
        manager.close()
        logging.getLogger("arelle").removeHandler(log_handler)

    return {"options": { "disclosure_system": disclosure_system,
                         "infer_decimals": infer_decimals,
                         "calc_linkbase": calc_linkbase,
                         "utr": utr },
            "results": log_handler.messages}


def cmd_parser():
    parser = argparse.ArgumentParser(description='Validate XBRL')
    parser.add_argument('-s','--disclosure_system')
    parser.add_argument('--infer_decimals', action='store_true')
    parser.add_argument('--calc_linkbase', action='store_true')
    parser.add_argument('--utr', action='store_true')
    parser.add_argument('-f','--file', dest='file_or_path', required=True)
    return parser

def get_options():
    return cmd_parser().parse_args(sys.argv[1:])

def run_validation():
    return validate(**vars(get_options()))

if __name__ == "__main__":
    v = run_validation()
    print(json.dumps(v))
