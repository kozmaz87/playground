# -*- mode: python ; coding: utf-8 -*-

import pkg_resources
import os
import sys
from PyInstaller.utils.hooks import collect_submodules, collect_data_files

block_cipher = None

hiddenimports = set()

hiddenimports = hiddenimports | set(collect_submodules('pyface.ui.qt4'))
hiddenimports = hiddenimports | set(collect_submodules('PyQt5'))
hiddenimports = hiddenimports | set(collect_submodules('tvtk.pyface.ui.qt4'))

# work around the following bug https://github.com/pypa/setuptools/issues/1963
hiddenimports.add('pkg_resources.py2_warn')

# collect data files like images from pyface, mayavi, and tvtk such that they are displayed in the UI
datas = set()
datas = datas | set(collect_data_files('traitsui'))
datas = datas | set(collect_data_files('pyface'))

librarylocation = os.path.join(os.path.normpath(sys.exec_prefix), 'Library')

#datas = datas | {
#    ('{}/resources/*.*'.format(librarylocation), 'PyQt5/Qt/bin/'),
#    ('{}/plugins/platforms'.format(librarylocation), 'platforms'),
#    ('{}/plugins/imageformats'.format(librarylocation), 'imageformats'),
#    ('{}/plugins/styles'.format(librarylocation), 'styles')
#}

# List of packages that should have there Distutils entrypoints included.
hook_ep_packages = dict()
ep_packages = ['traitsui.toolkits', 'pyface.toolkits', 'tvtk.toolkits']

if ep_packages:
    for ep_package in ep_packages:
        for ep in pkg_resources.iter_entry_points(ep_package):
            if ep.name in ('null', 'wx'):
                continue
            if ep_package in hook_ep_packages:
                package_entry_point = hook_ep_packages[ep_package]
            else:
                package_entry_point = []
                hook_ep_packages[ep_package] = package_entry_point
            package_entry_point.append("{} = {}:{}".format(ep.name, ep.module_name, ep.attrs[0]))
            hiddenimports.add(ep.module_name)

    try:
        os.mkdir('./generated')
    except FileExistsError:
        pass

    with open("./generated/pkg_resources_hook.py", "w") as f:
        f.write("""# Runtime hook generated from spec file to support pkg_resources entrypoints.
ep_packages = {}

if ep_packages:
    import pkg_resources
    default_iter_entry_points = pkg_resources.iter_entry_points

    def hook_iter_entry_points(group, name=None):
        if group in ep_packages and ep_packages[group]:
            eps = ep_packages[group]
            for ep in eps:
                parsedEp = pkg_resources.EntryPoint.parse(ep)
                parsedEp.dist = pkg_resources.Distribution()
                yield parsedEp
        else:
            return default_iter_entry_points(group, name)

    pkg_resources.iter_entry_points = hook_iter_entry_points
""".format(hook_ep_packages))

a = Analysis(['buittoneditor.py'],
             pathex=['C:\\Users\\Ubul\\Projects\\playground'],
             binaries=[],
             datas=list(datas),
             hiddenimports=list(hiddenimports),
             hookspath=[],
             runtime_hooks = ['./generated/pkg_resources_hook.py'],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='buittoneditor',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='buittoneditor')
