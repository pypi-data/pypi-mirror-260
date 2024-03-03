# -*- coding: utf-8 -*-


# start delvewheel patch
def _delvewheel_patch_1_5_2():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'brainpylib.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-brainpylib-0.3.0')
        if os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-brainpylib-0.3.0')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(ctypes.c_wchar_p(lib_path), None, 0x00000008):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_5_2()
del _delvewheel_patch_1_5_2
# end delvewheel patch

__all__ = [
    '__version__',
    '__brainpy_minimal_version__',
    '__minimal_taichi_version__',
    'check_brainpy_version',
]

__version__ = "0.3.0"
__brainpy_minimal_version__ = '2.5.0'
__minimal_taichi_version__ = (1, 7, 0)

import os
import platform
import sys
import ctypes

with open(os.devnull, 'w') as devnull:
    os.environ["TI_LOG_LEVEL"] = "error"
    old_stdout = sys.stdout
    sys.stdout = devnull
    try:
        import taichi as ti  # noqa
    except ModuleNotFoundError:
        raise ModuleNotFoundError(
            f'We need taichi=={__minimal_taichi_version__}. '
            f'Currently you can install taichi=={__minimal_taichi_version__} through:\n\n'
            '> pip install taichi==1.7.0 -U'
            # '> pip install -i https://pypi.taichi.graphics/simple/ taichi-nightly'
        )
    finally:
        sys.stdout = old_stdout
del old_stdout, devnull

# check Taichi version
if ti.__version__ != __minimal_taichi_version__:
    raise RuntimeError(
        f'We need taichi=={__minimal_taichi_version__}. '
        f'Currently you can install taichi=={__minimal_taichi_version__} through taichi-nightly:\n\n'
        '> pip install taichi==1.7.0 -U'
    )

# update Taichi runtime and C api
taichi_path = ti.__path__[0]
taichi_c_api_install_dir = os.path.join(taichi_path, '_lib', 'c_api')
os.environ.update({'TAICHI_C_API_INSTALL_DIR': taichi_c_api_install_dir,
                   'TI_LIB_DIR': os.path.join(taichi_c_api_install_dir, 'runtime')})

# link the Taichi C api
if platform.system() == 'Windows':
    dll_path = os.path.join(os.path.join(taichi_c_api_install_dir, 'bin/'), 'taichi_c_api.dll')
    try:
        ctypes.CDLL(dll_path)
    except OSError:
        raise OSError(f'Can not find {dll_path}')
    del dll_path
elif platform.system() == 'Linux':
    so_path = os.path.join(os.path.join(taichi_c_api_install_dir, 'lib/'), 'libtaichi_c_api.so')
    try:
        ctypes.CDLL(so_path)
    except OSError:
        raise OSError(f'Can not find {so_path}')
    del so_path

del os, sys, platform, ti, ctypes, taichi_path, taichi_c_api_install_dir

# find brainpylib in the installed package
try:
    import pkg_resources
    installed_libs = {}
    for i in pkg_resources.working_set:
        if i.key == 'brainpylib':
            installed_libs[i.key] = f'brainpylib only for CPU, version = {i.version}, location = {i.location}'
        if i.key == 'brainpylib-cu11x':
            installed_libs[i.key] = (f'brainpylib-cu11x only for CUDA 11.x, '
                                     f'version = {i.version}, location = {i.location}')
        if i.key == 'brainpylib-cu12x':
            installed_libs[i.key] = (f'brainpylib-cu12x only for CUDA 12.x, '
                                     f'version = {i.version}, location = {i.location}')
    if len(installed_libs) > 1:
        libs = "\n- ".join(list(installed_libs.values()))
        raise RuntimeError(
            'You have multiple brainpylib installed, please keep only one of them. The installed brainpylib are:'
            f'\n- {libs}'
        )
    del installed_libs, pkg_resources, i
except:
    pass


def check_brainpy_version():
    import brainpy as bp
    if bp.__version__ < __brainpy_minimal_version__:
        raise RuntimeError(f'brainpylib needs brainpy >= {__brainpy_minimal_version__}, please upgrade it. ')
