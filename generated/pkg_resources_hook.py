# Runtime hook generated from spec file to support pkg_resources entrypoints.
ep_packages = {'traitsui.toolkits': ['qt = traitsui.qt4:toolkit', 'qt4 = traitsui.qt4:toolkit'], 'pyface.toolkits': ['qt = pyface.ui.qt4.init:toolkit_object', 'qt4 = pyface.ui.qt4.init:toolkit_object'], 'tvtk.toolkits': ['qt = tvtk.pyface.ui.qt4.init:toolkit_object', 'qt4 = tvtk.pyface.ui.qt4.init:toolkit_object']}

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
