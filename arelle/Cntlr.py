'''
Created on Oct 3, 2010

@author: Mark V Systems Limited
(c) Copyright 2010 Mark V Systems Limited, All rights reserved.
'''
import tempfile, os, pickle, sys, logging, gettext
from arelle import ModelManager
from arelle.Locale import getLanguageCodes
from arelle import config

class Cntlr:

    __version__ = "0.0.4"
    
    def __init__(self, logFileName=None, logFileMode=None, logFileEncoding=None, logFormat=None):
        self.userAppDir = config.data_dir()
        self.hasClipboard = config.has_clipboard()
        self.hasWin32gui = False
        if sys.platform == "darwin":
            self.isMac = True
            self.isMSW = False
            self.contextMenuClick = "<Button-2>"
            self.updateURL = "http://arelle.org/downloads/8"
        elif sys.platform.startswith("win"):
            self.isMac = False
            self.isMSW = True

            try:
                import win32gui
                self.hasWin32gui = True # active state for open file dialogs
            except ImportError:
                pass
            self.contextMenuClick = "<Button-3>"
            if "64 bit" in sys.version:
                self.updateURL = "http://arelle.org/downloads/9"
            else: # 32 bit
                self.updateURL = "http://arelle.org/downloads/10"
        else: # Unix/Linux
            self.isMac = False
            self.isMSW = False
            self.contextMenuClick = "<Button-3>"
        self.moduleDir = os.path.dirname(__file__)
        # for python 3.2 remove __pycache__
        if self.moduleDir.endswith("__pycache__"):
            self.moduleDir = os.path.dirname(self.moduleDir)

        self.configDir = config.config_dir()
        self.imagesDir = config.images_dir()
        self.localeDir = config.locale_dir()
        # assert that app dir must exist
        if not os.path.exists(self.userAppDir):
            os.makedirs(self.userAppDir)
        # load config if it exists
        self.config = config.load_user_config()
        if not self.config:
            self.config = {
                'fileHistory': [],
                'windowGeometry': "{0}x{1}+{2}+{3}".format(800, 500, 200, 100),                
            }
            
        # start language translation for domain
        try:
            gettext.translation("arelle", self.localeDir, getLanguageCodes()).install()
        except Exception as msg:
            gettext.install("arelle", self.localeDir)

        from arelle.WebCache import WebCache
        self.webCache = WebCache(self, self.config.get("proxySettings"))
        self.modelManager = ModelManager.initialize(self)
        
        if logFileName: # use default logging
            self.logger = logging.getLogger("arelle")
            if logFileName == "logToPrint":
                self.logHandler = LogToPrintHandler()
            else:
                self.logHandler = logging.FileHandler(filename=logFileName, 
                                                      mode=logFileMode if logFileMode else "w", 
                                                      encoding=logFileEncoding if logFileEncoding else "utf-8")
            self.logHandler.level = logging.DEBUG
            self.logHandler.setFormatter(logging.Formatter(logFormat if logFormat else "%(asctime)s [%(messageCode)s] %(message)s - %(file)s %(sourceLine)s \n"))
            self.logger.addHandler(self.logHandler)
        else:
            self.logger = None
            
    def addToLog(self, message, messageCode="", file="", sourceLine=""):
        # if there is a default logger, use it with dummy file name and arguments
        if self.logger is not None:
            self.logger.info(message, extra={"messageCode":messageCode,"file":file,"sourceLine":sourceLine})
        else:
            print(message) # allows printing on standard out
            
    def showStatus(self, message, clearAfter=None):
        # dummy status line for batch operation
        pass
    
    def close(self, saveConfig=False):
        if saveConfig:
            self.saveConfig()
        if self.logger is not None:
            self.logHandler.close()
        
    def saveConfig(self):
        config.save_user_config(self.config)
            
    # default non-threaded viewModelObject                 
    def viewModelObject(self, modelXbrl, objectId):
        modelXbrl.viewModelObject(objectId)
            
    def reloadViews(self, modelXbrl):
        pass
    
    def rssWatchUpdateOption(self, **args):
        pass
        
    # default web authentication password
    def internet_user_password(self, host, realm):
        return ('myusername','mypassword')
    
    # if no text, then return what is on the clipboard, otherwise place text onto clipboard
    def clipboardData(self, text=None):
        if self.hasClipboard:
            try:
                if sys.platform == "darwin":
                    import subprocess
                    if text is None:
                        p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
                        retcode = p.wait()
                        text = p.stdout.read()
                        return text
                    else:
                        p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
                        p.stdin.write(text)
                        p.stdin.close()
                        retcode = p.wait()
                elif sys.platform.startswith("win"):
                    import win32clipboard
                    win32clipboard.OpenClipboard()
                    if text is None:
                        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT):
                            return win32clipboard.GetClipboardData().decode("utf8")
                    else:
                        win32clipboard.EmptyClipboard()
                        win32clipboard.SetClipboardData(win32clipboard.CF_TEXT, text.encode("utf8"))
                    win32clipboard.CloseClipboard()
                else: # Unix/Linux
                    import gtk
                    clipbd = gtk.Clipboard(display=gtk.gdk.display_get_default(), selection="CLIPBOARD")
                    if text is None:
                        return clipbd.wait_for_text().decode("utf8")
                    else:
                        clipbd.set_text(text.encode("utf8"), len=-1)
            except Exception:
                pass
        return None

class LogToPrintHandler(logging.Handler):
    def emit(self, logRecord):
        print(self.format(logRecord))



