import maya.cmds as cmds
cmds.select(hi=True)
selObjList = cmds.ls(sl=True, shapes=True)
for selObj in selObjList:
    shaderEngine1 = cmds.listConnections(selObj, type='shadingEngine')
    shaderEngine = cmds.listConnections(shaderEngine1, type='lambert')
    objShader = ''
    selObjpath = selObj + '.shop_materialpath'
    shaderEngine = shaderEngine[0]
    objShader = '/mat/'+shaderEngine
    cmds.addAttr(selObj, shortName='asn', longName='shop_materialpath', dataType='string')
    cmds.setAttr(selObjpath,objShader,type='string')
