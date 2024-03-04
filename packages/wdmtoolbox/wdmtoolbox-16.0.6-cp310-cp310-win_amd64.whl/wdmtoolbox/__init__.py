"""Package __init__.py.

Taken from numpy that they use to import openblas.

Helper to preload windows DLLs to prevent DLL not found errors.
Once a DLL is preloaded, its namespace is made available to any
subsequent DLL.
"""


# start delvewheel patch
def _delvewheel_patch_1_5_2():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, '.'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_5_2()
del _delvewheel_patch_1_5_2
# end delvewheel patch

import glob
import os
import sysconfig

if os.name == "nt":
    from ctypes import WinDLL

    basedir = sysconfig.get_path("purelib")
    libs_dir = [os.path.abspath(os.path.join(basedir, "_wdm_lib", ".libs"))]
    libs_dir += [os.path.abspath(os.path.join(basedir, "wdmtoolbox", ".libs"))]

    for lib in libs_dir:
        for filename in glob.glob(os.path.join(lib, "*.dll")):
            if os.path.exists(filename):
                _ = WinDLL(os.path.abspath(filename))