import maya.cmds as cmds
import os
cmds.select(hi=True)
selObjList = cmds.ls(sl=True,type = 'phong')
material_name = []
final_txt = ''
txtpath = 'C:/temp/txt/'
for node in selObjList:
    try:
        file_tex = cmds.listConnections(node + '.color')
        file_tex_path = cmds.getAttr(file_tex[0] + '.fileTextureName')
        final_txt = final_txt + str(node) + '-tex-' + str(file_tex_path)+'\n'
    except:
        pass
if not os.path.exists(txtpath):
    os.makedirs(txtpath)
f = open(txtpath+'test.txt','w')
f.write(final_txt)
f.close()
