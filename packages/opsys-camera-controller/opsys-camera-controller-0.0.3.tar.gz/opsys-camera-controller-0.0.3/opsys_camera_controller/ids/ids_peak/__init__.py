import os
import sys

if "IDS_PEAK_GENERIC_SDK_PATH" not in os.environ:
    raise RuntimeError(
        "Required environment variable "
        "IDS_PEAK_GENERIC_SDK_PATH does not exist! "
        "Please (re)install peak "
        "or provide the SDK root path of "
        "peak "
        "(<peak-Installation-Directory>/sdk/) "
        "manually via environment variable IDS_PEAK_GENERIC_SDK_PATH!")

GENERIC_SDK_PATH = os.environ[
    "IDS_PEAK_GENERIC_SDK_PATH"]
BUILD_ARCHITECTURE = "x86_64"
DLL_DIRECTORIES = [
    os.path.join(
        GENERIC_SDK_PATH,
        "api",
        "lib", BUILD_ARCHITECTURE
    ),
]
PATHSEP_STRING = "".join(
    f"{os.pathsep}{dll_dir}" for dll_dir in DLL_DIRECTORIES)

if (sys.version_info[0] < 3) or ((sys.version_info[0] == 3) and (sys.version_info[1] < 8)):
    os.environ["Path"] += PATHSEP_STRING
else:
    for dll_dir in DLL_DIRECTORIES:
        os.add_dll_directory(dll_dir)
    # Workaround for Conda Python 3.8 environments under Windows.PATHSEP_STRING
    # Although Python changed the DLL search mechanism in Python 3.8,
    # Windows Conda Python 3.8 environments still use the old mechanism...
    os.environ["Path"] += PATHSEP_STRING


try:
    from . import ids_peak
except ImportError as previousError:
    err = ImportError(
        "Could not load the python extension module! Either the shared "
        "library \"ids_peak\" could not be found or the library "
        "version you are using is older than the bindings (expected "
        "v1."
        "6."
        "2."
        "0)"
    )
    err.name = previousError.name
    err.path = previousError.path
    raise err from None

