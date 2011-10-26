import os
import os.path as path
import sys
import pickle

import appdirs

overrides = {}

def data_dir():
    return overrides.get('data_dir', None) or \
        os.getenv("ARELLE_DATA_DIR") or \
        appdirs.user_data_dir("Arelle")

def cache_dir():
    return overrides.get('cache_dir', None) or \
        os.getenv("ARELLE_CACHE_DIR") or \
        appdirs.user_cache_dir("Arelle")

def base_dir():
    d = path.dirname(__file__)
    if d.endswith("__pycache__"):
        d = path.dirname(d)
        
    if d.endswith("python32.zip/arelle"):
        d = path.normpath(path.join(d, '..', '..', '..'))
    elif d.endswith("library.zip\\arelle"):
        d = path.normpath(path.join(d, '..', '..'))
        
    return d

def resource_dir():
    return overrides.get('resource_dir', None) or \
        os.getenv("ARELLE_RESOURCE_DIR") or \
        base_dir()

def config_dir():
    return overrides.get('config_dir', None) or \
        os.getenv("ARELLE_CONFIG_DIR") or \
        path.join(resource_dir(), "config")

def images_dir():
    return overrides.get('images_dir', None) or \
        os.getenv("ARELLE_IMAGES_DIR") or \
        path.join(resource_dir(), "images")

def locale_dir():
    return overrides.get('locale_dir', None) or \
        os.getenv("ARELLE_LOCALE_DIR") or \
        path.join(resource_dir(), "locale")

def user_config_file():
    return overrides.get('config_file', None) or \
        os.getenv("ARELLE_CONFIG_FILE") or \
        path.join(data_dir(), "config.pickle")

def load_user_config():
    try:
        with open(config_file(), 'rb') as f:
            return pickle.load(f)
    except Exception:
        return None

def save_user_config(c):
    try:
        with open(config_file(), 'wb') as f:
            pickle.dump(c, f, pickle.HIGHEST_PROTOCOL)
            return True
    except Exception:
        return False

def has_clipboard():
    if sys.platform == "darwin":
        return True
    elif sys.platform == "win32":
        try:
            import win32clipboard
            return True
        except ImportError:
            return False
    else:
        try:
            import gtk
            return True
        except ImportError:
            return False

