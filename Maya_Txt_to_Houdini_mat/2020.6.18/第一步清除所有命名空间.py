import maya.cmds as cmds

for i in cmds.namespaceInfo(recurse=True,listOnlyNamespaces=True):
    try:
        if('UI' not in i and 'shared' not in i):
            cmds.namespace(mergeNamespaceWithParent=True,removeNamespace=i)
    except:
        pass