from cx_Freeze import setup, Executable
import sys
if sys.platform == "win32":
    base = "Win32GUI"
    includeDependencies = []
else:
    base = None
    includeDependencies = []
includePersonalFiles = [ ("data","data"), ("README.txt","README.txt") ]
includeFiles = includeDependencies + includePersonalFiles
buildOptions = dict( include_files = includeFiles, optimize = 2, compressed = True )
setup( name = "Nexus",
       version = "1.0",
       description = "Nexus - Data Processor Construct",
       options = dict(build_exe = buildOptions),
       executables = [Executable("nexus.py", base = base)] )

