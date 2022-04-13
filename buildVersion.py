'''
Created on May 28, 2011

@author: Mark V Systems Limited
(c) Copyright 2011 Mark V Systems Limited, All rights reserved.

This module emits the version.py file contents which are used in the
build process to indicate the time that this version was built.

'''
import datetime, sys, subprocess, os
arelleMajorVersion = 1 # major verison = 1 (python), 2 (cython)

if __name__ == "__main__":
    is64BitPython = sys.maxsize == 0x7fffffffffffffff
    timestamp = datetime.datetime.utcnow()
    dateYr = timestamp.strftime("%Y")
    dateDashYmd = timestamp.strftime("%Y-%m-%d")
    dateDotYmd = timestamp.strftime("%Y.%m.%d")
    dateDashYmdHmUtc = timestamp.strftime("%Y-%m-%d %H:%M UTC")
    
    versionPy = ("'''\n"
                 "This module represents the time stamp when Arelle was last built\n"
                 "\n"
                 "@author: Mark V Systems Limited\n"
                 "(c) Copyright {0} Mark V Systems Limited, All rights reserved.\n"
                 "\n"
                 "'''\n"
                 "__version__ = '{1}.{2}'  # number version of code base and date compiled\n"
                 "version = '{3}'  # string version of date compiled\n"
                 "copyrightLatestYear = '{0}'  # string version of year compiled\n"
                 ).format(dateYr, arelleMajorVersion, dateDotYmd, dateDashYmdHmUtc)
                 
    versionTxt = dateDashYmdHmUtc

    try:
        arelleCommit = subprocess.check_output(["git", "show", "--format='%h'", "--no-patch"]).decode("utf-8").strip()
        os.chdir("arelle/plugin/EdgarRenderer")
        edgarRendererCommit = subprocess.check_output(["git", "show", "--format='%h'", "--no-patch"]).decode("utf-8").strip()
        os.chdir("../../..")
        versionPy += ("arelleCommit = {0} # git Arelle commit \n"
                      "edgarRendererCommit = {1} # git EdgarRenderer commit \n"
                      ).format(arelleCommit, edgarRendererCommit)
        versionTxt += ("\narelleCommit {0} "
                       "\nedgarRendererCommit {1}"
                      ).format(arelleCommit[1:-1], edgarRendererCommit[1:-1])
    except Exception:
        pass

    with open("arelle/Version.py", "w") as fh:
        fh.write(versionPy)
        
    with open("version.txt", "w") as fh:
        fh.write(versionTxt)
        

    # add name suffix, like ER3 or TKTABLE
    if len(sys.argv) > 1 and sys.argv[1] and sys.platform not in ("linux",):
        dateDashYmd += "-" + sys.argv[1]
        
    if sys.platform == "darwin":
        with open("buildRenameDmg.sh", "w") as fh:
            fh.write("cp dist_dmg/arelle.dmg dist/arelle-macOS-{}.dmg\n".format(dateDashYmd))
    if sys.platform == "linux2":
        with open("buildRenameLinux-x86_64.sh", "w") as fh:
            fh.write("mv dist/exe.linux-x86_64-{}.{}.tar.gz dist/arelle-linux-x86_64-{}.tgz\n"
                     .format(sys.version_info[0], sys.version_info[1], dateDashYmd))
    elif sys.platform == "linux": # python 3.3
        if len(sys.argv) > 1 and sys.argv[1]:
            sysName = sys.argv[1]
        else:
            sysName = "linux"
        with open("buildRenameLinux-x86_64.sh", "w") as fh:
            fh.write("mv dist/exe.linux-x86_64-{}.{}.tgz dist/arelle-{}-x86_64-{}.tgz\n"
                     .format(sys.version_info[0], sys.version_info[1], 
                             sysName, dateDashYmd))
    elif sys.platform == "sunos5":
        with open("buildRenameSol10Sun4.sh", "w") as fh:
            fh.write("mv dist/exe.solaris-2.10-sun4v{0}-{1}.{2}.tgz dist/arelle-solaris10-sun4{0}-{3}.tgz\n"
                     .format(".64bit" if is64BitPython else "",
                             sys.version_info[0],sys.version_info[1], 
                             dateDashYmd))
    elif sys.platform.startswith("win"):
        renameCmdFile = "buildRenamer.bat"
        with open("buildRenameX86.bat", "w") as fh:
            fh.write("rename dist\\arelle-win-x86.exe arelle-win-x86-{}.exe\n".format(dateDashYmd))
        with open("buildRenameX64.bat", "w") as fh:
            fh.write("rename dist\\arelle-win-x64.exe arelle-win-x64-{0}.exe\n"
                     "rename dist\\arelle-win-x64.zip arelle-win-x64-{0}.zip\n"
                     .format(dateDashYmd))
        with open("buildRenameSvr27.bat", "w") as fh:
            fh.write("rename dist\\arelle-svr-2.7.zip arelle-svr-2.7-{}.zip\n".format(dateDashYmd))
        with open("buildRenameZip32.bat", "w") as fh:
            fh.write("rename dist\\arelle-cmd32.zip arelle-cmd32-{}.zip\n".format(dateDashYmd))
        with open("buildRenameZip64.bat", "w") as fh:
            fh.write("rename dist\\arelle-cmd64.zip arelle-cmd64-{}.zip\n".format(dateDashYmd))
