"""Wrapper for fTetWild."""


# start delvewheel patch
def _delvewheel_patch_1_5_2():
    import os
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pytetwild.libs'))
    if os.path.isdir(libs_dir):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_5_2()
del _delvewheel_patch_1_5_2
# end delvewheel patch

from ._version import __version__  # noqa: F401
from .pytetwild import tetrahedralize, tetrahedralize_pv  # noqa: F401