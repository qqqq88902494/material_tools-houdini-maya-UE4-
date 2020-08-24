import maya.cmds as cmds
import os
cmds.select(hi=True)
selObjList = cmds.ls(sl=True,type = 'lambert')
material_name = []
final_txt = ''
txtpath = 'C:/temp/txt/'
for node in selObjList:
    file_tex = cmds.listConnections(node + '.color')
    file_tex_type = cmds.nodeType(file_tex)
    if ( file_tex != None and str(file_tex_type) == 'file' ):
        try:
            file_tex = cmds.listConnections(node + '.color')
            file_tex_path = cmds.getAttr(file_tex[0] + '.fileTextureName')
            final_txt = final_txt + str(node) + '-tex-' + str(file_tex_path)+'\n'
            #print final_txt
        except:
            pass
    else:
        try:
            diff_c_number = cmds.getAttr(node+'.color')[0]
            final_txt = final_txt + str(node) + '-num-' + str(diff_c_number)+'\n'
            #print final_txt
        except:
            pass
if not os.path.exists(txtpath):
    os.makedirs(txtpath)
f = open(txtpath+'test.txt','w')
f.write(final_txt)
f.close()