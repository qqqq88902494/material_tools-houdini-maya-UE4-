
import maya.cmds as cmds
StartShader = 'aiStandardSurface'
EndShader = 'blinn'

diff_w_parm1 = '.base'
diff_w_parm2 = '.diffuse'

diff_color1 = '.baseColor'
diff_color2 = '.color'

metalness1 = '.metalness'
metalness2 = '.reflectivity'

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

del_mat_list = []
del_Displace_Utility_list = []

for node in ai_list:
    try:   
        new_shader = cmds.shadingNode(EndShader,n=EndShader+'_'+ str(node) , asShader=True)
        old_shadingEngine = cmds.listConnections( node + '.outColor')
        for shading_node in old_shadingEngine:
            cmds.connectAttr(str(new_shader) + '.outColor' , str(shading_node) + '.surfaceShader',force=True)
        
        #diffuse_weight
        diff_w_file = cmds.listConnections( node + diff_w_parm1)
        if ( diff_w_file != None ):
            cmds.connectAttr(str(diff_w_file[0]) + '.outAlpha' , str(new_shader) + diff_w_parm2 , force=True)
        else:  
            diff_w_number = cmds.getAttr(node+diff_w_parm1)
            cmds.setAttr(new_shader + diff_w_parm2 , diff_w_number)
            
            
        #diffuse_color
        diff_c_file = cmds.listConnections( node + diff_color1)
        diff_c_file_type = cmds.nodeType(diff_c_file)
        if ( diff_c_file != None and str(diff_c_file_type) == 'file' ):
            cmds.connectAttr(str(diff_c_file[0]) + '.outColor' , str(new_shader) + diff_color2 , force=True)
        else:  
            diff_c_number = cmds.getAttr(node+diff_color1)
            cmds.setAttr(new_shader + diff_color2 , diff_c_number[0][0],diff_c_number[0][1],diff_c_number[0][2],type="double3")
    except:
        continue