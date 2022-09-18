from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import platform, datetime


def get_version():
    """
    Utility function to return the current version of the library, as defined
    by the version string in the arelle's _pkg_meta.py file. The format follows
    the standard Major.Minor.Fix notation.
    
    To compile for arelle (python) debugging (leaves .so in arelle where it is needed by debugger):

    cd src-cython
    src-cython hermf$ touch arelle_cython/arelle.arelle_c.pyx; time python3.9 setup-arelle_C.py build_ext --inplace > ~/temp/log.txt 2>&1
    
    copy rlglen /usr/include/x86_64-linux-gnu/c++/5/bits to mac /usr/include ...

    :return: The version string in the standard Major.Minor.Fix notation.
    :rtype: str
    """
    import imp

    source_dir = 'arelle'

    with open('{}/_pkg_meta.py'.format(source_dir), 'rb') as fp:
        mod = imp.load_source('_pkg_meta', source_dir, fp)

    return mod.version

# convert XMLCh constants from strings
import re
wchStr = re.compile(r'((.*)\s+(XMLCh\[\]|hash_t)\s+(\w+)\s(.*))([hx]\")([^"]*)(")(.*)$')
splWChars = {"&": "chAmpersand", "*": "chAsterisk", "@": "chAt", "\\": "chBackSlash", "!": "chBang", "^": "chCaret",
             ">": "chCloseAngle", "}": "chCloseCurly", ")": "chCloseParen", "]": "chCloseSquare", ":": "chColon",
             ",": "chComma", "-": "chDash", "$": "chDollarSign", "\"": "chDoubleQuote", "=": "chEqual", "/": "chForwardSlash",
             "`": "chGrave", "": "chNEL", "<": "chOpenAngle", "{": "chOpenCurly", "(": "chOpenParen", "[": "chOpenSquare",
             "%": "chPercent", ".": "chPeriod", "|": "chPipe", "+": "chPlus", "#": "chPound", "?": "chQuestion",
             "'": "chSingleQuote", " ": "chSpace", ";": "chSemiColon", "~": "chTilde", "_": "chUnderscore",
             '"': "chDoubleQuote"}
with open("arelle_cython/arelle_c/consts.pxi", "wt") as fWt:
    with open("arelle_cython/arelle_c/consts.src", "rt") as fRd:
        while True:
            r = fRd.readline()
            if len(r) == 0:
                break
            while r.endswith("\\\n"):
                continuation = fRd.readline()
                if len(continuation) == 0:
                    break
                r = r[:-2] + continuation
            m = wchStr.match(r)
            if m is not None:
                s = m.group(7).replace('\\x22', '"') # allow \x22 to escape " character
                if m.group(6) == 'x"':
                    t = m.group(3).replace("[]", "[{}]".format(len(s)+1))
                    n = m.group(4)
                    r = '{} {} {}\n{}[:] = [{}{}chNull]\n'.format(
                        m.group(2), t, n, n,
                        ", ".join(("chLatin_" + c) if ("a" <= c <= "z" or "A" <= c <= "Z") else
                                  ("chDigit_" + c) if ("0" <= c <= "9") else
                                  splWChars.get(c, "?")
                                  for c in s),
                        ", " if s else "",
                        m.group(5))
                elif m.group(6) == 'h"':
                    r = '{}PyObject_Hash(u"{}"){} # hash of "{}"\n'.format(m.group(1), s, m.group(9), s)
            fWt.write(r)
        fWt.write("\n#generated by setup-arelle_c.py\n")
        fWt.write("cdef unicode uDateCompiled = u\"{}\"\n".format(datetime.datetime.utcnow().strftime("%Y.%m.%d")))

compile_extra_args = []
link_extra_args = []

if platform.system() == "Windows":
    compile_extra_args = ["/std:c++latest", "/EHsc"]
elif platform.system() == "Darwin":
    compile_extra_args = ['-std=c++11', "-mmacosx-version-min=10.9"]
    link_extra_args = ["-stdlib=libc++", "-mmacosx-version-min=10.9"]


setup( name="Arelle_c",
       version=get_version(),
       author='arelle.org',
       author_email='support@arelle.org',
       url='http://www.arelle.org',
       download_url='http://www.arelle.org/download',
       license='Apache-2',
       keywords=['xbrl'],
       description='An open source XBRL platform',
       long_description=open('README.md').read(),
       packages=[ "arelle_c" ],
       classifiers=[ 
        'Development Status :: 1 - Active',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache-2 License',
        'Natural Language :: English',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 3.5'
        ],
       cmdclass=dict( build_ext=build_ext ),
       ext_modules=[ Extension( "arelle.arelle_c",
                                [ "arelle_cython/arelle.arelle_c.pyx" ],
                                #include_dirs =['/usr/include/c++/4.2.1/tr1', '/usr/include/i386','/usr/include','/usr/local/include','/usr/include/sys'],
                                #include_dirs =['/Library/Developer/CommandLineTools/usr/include/c++/v1', '/usr/include/i386','/usr/include','/usr/local/include','/usr/include/sys'],
                                #include_dirs =['/Users/hermf/temp/include/fromLinux/c++/5.4.0', '/usr/include/i386','/usr/include','/usr/local/include','/usr/include/sys'],
                                #include_dirs =['/usr/local/include', '/Users/hermf/temp/include'],
                                library_dirs = ['/usr/local/lib'],
                                language="c++",
                                libraries=[ "stdc++",
                                            "xerces-c" ] ,
                                extra_compile_args=compile_extra_args,
                                extra_link_args=link_extra_args
                                ) ]
    )
