import maya.cmds as cmds
selObjList = cmds.ls(sl=True)
for sel in selObjList:
    cmds.select( clear=True )
    cmds.select(sel)
    for i in cmds.polyUVSet( query=True, allUVSets=True ):
        try:
            cmds.polyUVSet( currentUVSet=True,  uvSet=i)
            cmds.polyUVSet( delete=True )
        except:
            pass
