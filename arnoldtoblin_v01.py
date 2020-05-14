# _*_ coding:UTF-8 _*_
#by vfxmstc https://github.com/qqqq88902494
#email:410386656@qq.com
#maya2020
#tools_version:v01
#support:arnold to blin
#just select all materials and run it!
#you can change StartShader EndShader  or diff_color1  diff_color2  to other material,or wait for update~~~

import maya.cmds as cmds

StartShader = 'aiStandardSurface'
EndShader = 'blinn'

diff_w_parm1 = '.base'
diff_w_parm2 = '.diffuse'

diff_color1 = '.baseColor'
diff_color2 = '.color'

ai_list = cmds.ls(sl = True,type = StartShader) 

for node in ai_list:
    
    
    new_shader = cmds.shadingNode(EndShader,n=EndShader+'_'+ str(node) , asShader=True)
    old_shadingEngine = cmds.listConnections( node + '.outColor')
    for shading_node in old_shadingEngine:
        cmds.connectAttr(str(new_shader) + '.outColor' , str(shading_node) + '.surfaceShader',force=True)
    
    
    #diffuse_weight
    diff_w_file = cmds.listConnections( node + diff_w_parm1)
    if ( diff_w_file != None ):
        cmds.connectAttr(str(diff_w_file[0]) + '.outColor.outColorR' , str(new_shader) + diff_w_parm2 , force=True)
    else:  
        diff_w_number = cmds.getAttr(node+diff_w_parm1)
        cmds.setAttr(new_shader + diff_w_parm2 , diff_w_number)
        
        
    #diffuse_color
    diff_c_file = cmds.listConnections( node + diff_color1)
    if ( diff_c_file != None ):
        cmds.connectAttr(str(diff_c_file[0]) + '.outColor' , str(new_shader) + diff_color2 , force=True)
    else:  
        diff_c_number = cmds.getAttr(node+diff_color1)
        cmds.setAttr(new_shader + diff_color2 , diff_c_number[0][0],diff_c_number[0][1],diff_c_number[0][2],type="double3")
