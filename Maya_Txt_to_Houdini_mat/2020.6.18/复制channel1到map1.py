import maya.cmds as cmds
selObjList = cmds.ls(sl=True)
for sel in selObjList:
    try:
        cmds.polyCopyUV( sel,uvi="UVChannel_1",uvs="map1" ,ch=1)
    except:
        pass