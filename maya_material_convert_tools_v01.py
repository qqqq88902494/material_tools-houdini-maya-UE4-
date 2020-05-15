# _*_ coding:UTF-8 _*_
#by vfxmstc https://github.com/qqqq88902494
#email:410386656@qq.com
#maya2020
#tools_version:v01
#support:arnold to blin
#just select all materials and run it!


import maya.cmds as cmds

StartShader = 'aiStandardSurface'
EndShader = 'blinn'

diff_w_parm1 = '.base'
diff_w_parm2 = '.diffuse'

diff_color1 = '.baseColor'
diff_color2 = '.color'

spc_w_parm1 = '.specular'
spc_w_parm2 = '.specularRollOff'

spc_color1 = '.specularColor'
spc_color2 = '.specularColor'

spc_Roughness1 = '.specularRoughness'
spc_Roughness2 = '.eccentricity'

tran_color1 = '.opacity'
tran_color2 = '.transparency'

bump_color1 = '.normalCamera'
bump_color2 = '.normalCamera'

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
    
    #specular_weight
    spc_w_file = cmds.listConnections( node + spc_w_parm1)
    if ( spc_w_file != None ):
        cmds.connectAttr(str(spc_w_file[0]) + '.outColor.outColorR' , str(new_shader) + spc_w_parm2 , force=True)
    else:  
        spc_w_number = cmds.getAttr(node+spc_w_parm1)
        cmds.setAttr(new_shader + spc_w_parm2 , spc_w_number)
    
    #specular_color
    spc_c_file = cmds.listConnections( node + spc_color1)
    if ( spc_c_file != None ):
        cmds.connectAttr(str(spc_c_file[0]) + '.outColor' , str(new_shader) + spc_color2 , force=True)
    else:  
        spc_c_number = cmds.getAttr(node+spc_color1)
        cmds.setAttr(new_shader + spc_color2 , spc_c_number[0][0],spc_c_number[0][1],spc_c_number[0][2],type="double3")
   
    #specularRoughness
    spcrou_w_file = cmds.listConnections( node + spc_Roughness1)
    if ( spcrou_w_file != None ):
        cmds.connectAttr(str(spcrou_w_file[0]) + '.outColor.outColorR' , str(new_shader) + spc_Roughness2 , force=True)
    else:  
        spcrou_w_number = cmds.getAttr(node+spc_Roughness1)
        cmds.setAttr(new_shader + spc_Roughness2 , spcrou_w_number)
    
    #opacity_color
    tran_c_file = cmds.listConnections( node + tran_color1)
    if ( tran_c_file != None ):
        cmds.connectAttr(str(tran_c_file[0]) + '.outColor' , str(new_shader) + tran_color2 , force=True)
    else:  
        tran_c_number = cmds.getAttr(node+tran_color1)
        cmds.setAttr(new_shader + tran_color2 , (1-int(tran_c_number[0][0])),(1-int(tran_c_number[0][1])),(1-int(tran_c_number[0][2])),type="double3")  
    
    #normal_bump
    ainormap = cmds.listConnections( node + bump_color1)
    if ( ainormap != None ):
        ainormap_type = cmds.nodeType(ainormap[0])
        if(ainormap_type == 'aiNormalMap'):
            ainormap_file = cmds.listConnections( ainormap[0] + '.input')
            new_bump_node = cmds.shadingNode('bump2d',n='new_bump2d_' + str(ainormap_file[0]) , asShader=True)
            cmds.setAttr(str(ainormap_file[0]) + '.alphaIsLuminance' , 1)
            cmds.setAttr(str(new_bump_node) + '.bumpInterp' , 1)
            cmds.connectAttr(str(ainormap_file[0]) + '.outAlpha' , str(new_bump_node) + '.bumpValue' , force=True)
            cmds.connectAttr(str(new_bump_node) + '.outNormal' , str(new_shader) + bump_color2 , force=True)
            #cmds.delete(ainormap[0])
        if(ainormap_type == 'bump2d'):
            ainormap_file = cmds.listConnections( ainormap[0] + '.bumpValue')
            new_bump_node = cmds.shadingNode('bump2d',n='new_bump2d_' + str(ainormap_file[0]) , asShader=True)
            cmds.setAttr(str(ainormap_file[0]) + '.alphaIsLuminance' , 1)
            cmds.setAttr(str(new_bump_node) + '.bumpInterp' , 1)
            cmds.connectAttr(str(ainormap_file[0]) + '.outAlpha' , str(new_bump_node) + '.bumpValue' , force=True)
            cmds.connectAttr(str(new_bump_node) + '.outNormal' , str(new_shader) + bump_color2 , force=True)
    
    
    
    
    
    cmds.delete(node)
