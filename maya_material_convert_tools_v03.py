import maya.cmds as cmds
import webbrowser 

def open_help(self):
    webbrowser.open_new_tab('https://github.com/qqqq88902494/maya_material_convert_tools')

def select_Anorld(self):
    cmds.select(cl=True)
    arnold_list = cmds.ls(type = 'aiStandardSurface')
    for node in arnold_list:
        cmds.select(node,add=True)
        
def select_Redshift(self):
    cmds.select(cl=True)
    redshift_list = cmds.ls(type = 'RedshiftMaterial')
    for node in redshift_list:
        cmds.select(node,add=True)

def AnorldToRedshift(self):
    
    StartShader = 'aiStandardSurface'
    EndShader = 'RedshiftMaterial'
    
    
    diff_color1 = '.baseColor'
    diff_color2 = '.diffuse_color'
    
    metalness1 = '.metalness'
    metalness2 = '.refl_metalness'
    
    spc_w_parm1 = '.specular'
    spc_w_parm2 = '.refl_weight'
    
    spc_color1 = '.specularColor'
    spc_color2 = '.refl_color'
    
    spc_Roughness1 = '.specularRoughness'
    spc_Roughness2 = '.refl_roughness'
    
    tran_color1 = '.opacity'
    tran_color2 = '.opacity_color'
    
    bump_color1 = '.normalCamera'
    bump_color2 = '.bump_input'
    
    ai_list = cmds.ls(sl = True,type = StartShader)
    
    del_mat_list = []
    del_Displace_Utility_list = []
    
    for node in ai_list:
        new_shader = cmds.shadingNode(EndShader,n='Rs'+'_'+ str(node) , asShader=True)
        old_shadingEngine = cmds.listConnections( node + '.outColor')
        for shading_node in old_shadingEngine:
            cmds.connectAttr(str(new_shader) + '.outColor' , str(shading_node) + '.surfaceShader',force=True)
            Displace_Utility = cmds.listConnections( shading_node + '.displacementShader')
            if ( Displace_Utility[0] != None ):
                new_Displace_Utility = cmds.shadingNode('RedshiftDisplacement',n='new_RsDis_' + str(Displace_Utility[0]) , asShader=True)
                if(cmds.nodeType(Displace_Utility[0]) == 'displacementShader'):
                    Displace_tex_file = cmds.listConnections( Displace_Utility[0] + '.displacement')
                    cmds.setAttr(str(new_Displace_Utility) + '.scale' , 0.1)
                    for Displace_tex_file_node in Displace_tex_file:
                        Displace_tex_file_node_type = cmds.nodeType(Displace_tex_file_node)
                        if(Displace_tex_file_node_type == 'file'):
                            cmds.connectAttr(str(Displace_tex_file_node) + '.outColor' , str(new_Displace_Utility) + '.texMap' , force=True)
                            cmds.connectAttr(str(new_Displace_Utility) + '.out' , shading_node + '.displacementShader' , force=True)
                if(cmds.nodeType(Displace_Utility[0]) == 'file'):
                    cmds.setAttr(str(new_Displace_Utility) + '.scale' , 0.1)
                    cmds.connectAttr(str(Displace_Utility[0]) + '.outColor' , str(new_Displace_Utility) + '.texMap', force=True)
                    cmds.connectAttr(str(new_Displace_Utility) + '.out' , shading_node + '.displacementShader' , force=True)
                        
                #del_Displace_Utility_list.append(Displace_Utility[0])
    
            
            #diffuse_color
            diff_c_file = cmds.listConnections( node + diff_color1)
            diff_c_file_type = cmds.nodeType(diff_c_file)
            if ( diff_c_file != None and str(diff_c_file_type) == 'file' ):
                cmds.connectAttr(str(diff_c_file[0]) + '.outColor' , str(new_shader) + diff_color2 , force=True)
            else:  
                diff_c_number = cmds.getAttr(node+diff_color1)
                cmds.setAttr(new_shader + diff_color2 , diff_c_number[0][0],diff_c_number[0][1],diff_c_number[0][2],type="double3")
        
            #metalness_weight
            metalness_w_file = cmds.listConnections( node + metalness1)
            metalness_w_file_type = cmds.nodeType(metalness_w_file)
            if ( metalness_w_file != None and str(metalness_w_file_type) == 'file' ):
                cmds.setAttr(new_shader + '.refl_fresnel_mode' , 2)
                cmds.connectAttr(str(metalness_w_file[0]) + '.outAlpha' , str(new_shader) + metalness2 , force=True)
            else:  
                metalness_w_number = cmds.getAttr(node+metalness1)
                cmds.setAttr(new_shader + metalness2 , metalness_w_number)
        
            
            #specular_weight
            spc_w_file = cmds.listConnections( node + spc_w_parm1)
            spc_w_file_type = cmds.nodeType(spc_w_file)
            if ( spc_w_file != None and str(spc_w_file_type) == 'file' ):
                cmds.connectAttr(str(spc_w_file[0]) + '.outAlpha' , str(new_shader) + spc_w_parm2 , force=True)
            else:  
                spc_w_number = cmds.getAttr(node+spc_w_parm1)
                cmds.setAttr(new_shader + spc_w_parm2 , spc_w_number)
            
            #specular_color
            spc_c_file = cmds.listConnections( node + spc_color1)
            spc_c_file_type = cmds.nodeType(spc_c_file)
            if ( spc_c_file != None and str(spc_c_file_type) == 'file'  ):
                cmds.connectAttr(str(spc_c_file[0]) + '.outColor' , str(new_shader) + spc_color2 , force=True)
            else:  
                spc_c_number = cmds.getAttr(node+spc_color1)
                cmds.setAttr(new_shader + spc_color2 , spc_c_number[0][0],spc_c_number[0][1],spc_c_number[0][2],type="double3")
           
            #specularRoughness
            spcrou_w_file = cmds.listConnections( node + spc_Roughness1)
            spcrou_w_file_type = cmds.nodeType(spcrou_w_file)
            if ( spcrou_w_file != None and str(spcrou_w_file_type) == 'file' ):
                cmds.connectAttr(str(spcrou_w_file[0]) + '.outAlpha' , str(new_shader) + spc_Roughness2 , force=True)
            if ( spcrou_w_file != None and str(spcrou_w_file_type) == 'aiRange' ):
                spcrou_w_file2 = cmds.listConnections( spcrou_w_file[0] + '.input')
                cmds.connectAttr(str(spcrou_w_file2[0]) + '.outAlpha' , str(new_shader) + spc_Roughness2, force=True)
            if ( spcrou_w_file == None):  
                spcrou_w_number = cmds.getAttr(node+spc_Roughness1)
                cmds.setAttr(new_shader + spc_Roughness2 , spcrou_w_number)
            
            #opacity_color
            tran_c_file = cmds.listConnections( node + tran_color1)
            tran_c_file_type = cmds.nodeType(tran_c_file)
            if ( tran_c_file != None and str(tran_c_file_type) == 'file' ):
                cmds.connectAttr(str(tran_c_file[0]) + '.outColor' , str(new_shader) + tran_color2 , force=True)
            else:  
                tran_c_number = cmds.getAttr(node+tran_color1)
                cmds.setAttr(new_shader + tran_color2 , int(tran_c_number[0][0]),int(tran_c_number[0][1]),int(tran_c_number[0][2]),type="double3")  
            
            #normal_bump
            ainormap = cmds.listConnections( node + bump_color1)
            if ( ainormap != None ):
                ainormap_type = cmds.nodeType(ainormap[0])
                if(ainormap_type == 'aiNormalMap'):
                    ainormap_file = cmds.listConnections( ainormap[0] + '.input')
                    new_bump_node = cmds.shadingNode('RedshiftBumpMap',n='new_Rsbump_' + str(ainormap_file[0]) , asTexture=True)
                    cmds.setAttr(str(ainormap_file[0]) + '.alphaIsLuminance' , 1)
                    cmds.connectAttr(str(ainormap_file[0]) + '.outColor' , str(new_bump_node) + '.input' , force=True)
                    cmds.connectAttr(str(new_bump_node) + '.out' , str(new_shader) + bump_color2 , force=True)
                    cmds.delete(ainormap[0])
                if(ainormap_type == 'bump2d'):
                    ainormap_file = cmds.listConnections( ainormap[0] + '.bumpValue')
                    new_bump_node = cmds.shadingNode('RedshiftBumpMap',n='new_Rsbump_' + str(ainormap_file[0]) , asTexture=True)
                    cmds.setAttr(str(ainormap_file[0]) + '.alphaIsLuminance' , 1)
                    cmds.connectAttr(str(ainormap_file[0]) + '.outColor' , str(new_bump_node) + '.input' , force=True)
                    cmds.connectAttr(str(new_bump_node) + '.out' , str(new_shader) + bump_color2 , force=True)
                    cmds.delete(ainormap[0])
            
            
            
            
            del_mat_list.append(node)
    
                
        for del_mat in set(del_mat_list):
            try:
                print 'delete ' + str(del_mat)
                cmds.delete(del_mat)
            except:
                continue
        for del_Displace_Utility in set(del_Displace_Utility_list):
            try:
                print 'delete ' + str(del_Displace_Utility)
                cmds.delete(del_Displace_Utility)
            except:
                continue


def AnorldToBlinn(self):
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
            
        #metalness_weight
        metalness_w_file = cmds.listConnections( node + metalness1)
        metalness_w_file_type = cmds.nodeType(metalness_w_file)
        if ( metalness_w_file != None and str(metalness_w_file_type) == 'file' ):
            cmds.connectAttr(str(metalness_w_file[0]) + '.outAlpha' , str(new_shader) + metalness2 , force=True)
        else:  
            metalness_w_number = cmds.getAttr(node+metalness1)
            cmds.setAttr(new_shader + metalness2 , metalness_w_number)
    
        #specular_weight
        spc_w_file = cmds.listConnections( node + spc_w_parm1)
        spc_w_file_type = cmds.nodeType(spc_w_file)
        if ( spc_w_file != None and str(spc_w_file_type) == 'file' ):
            cmds.connectAttr(str(spc_w_file[0]) + '.outAlpha' , str(new_shader) + spc_w_parm2 , force=True)
        else:  
            spc_w_number = cmds.getAttr(node+spc_w_parm1)
            cmds.setAttr(new_shader + spc_w_parm2 , spc_w_number)
            
        #specular_color
        spc_c_file = cmds.listConnections( node + spc_color1)
        spc_c_file_type = cmds.nodeType(spc_c_file)
        if ( spc_c_file != None and str(spc_c_file_type) == 'file'  ):
            cmds.connectAttr(str(spc_c_file[0]) + '.outColor' , str(new_shader) + spc_color2 , force=True)
        else:  
            spc_c_number = cmds.getAttr(node+spc_color1)
            cmds.setAttr(new_shader + spc_color2 , spc_c_number[0][0],spc_c_number[0][1],spc_c_number[0][2],type="double3")
         
        #specularRoughness
        spcrou_w_file = cmds.listConnections( node + spc_Roughness1)
        spcrou_w_file_type = cmds.nodeType(spcrou_w_file)
        if ( spcrou_w_file != None and str(spcrou_w_file_type) == 'file' ):
            cmds.connectAttr(str(spcrou_w_file[0]) + '.outAlpha' , str(new_shader) + spc_Roughness2 , force=True)
        else:  
            spcrou_w_number = cmds.getAttr(node+spc_Roughness1)
            cmds.setAttr(new_shader + spc_Roughness2 , spcrou_w_number)
        
        #opacity_color
        tran_c_file = cmds.listConnections( node + tran_color1)
        tran_c_file_type = cmds.nodeType(tran_c_file)
        if ( tran_c_file != None and str(tran_c_file_type) == 'file' ):
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
        del_mat_list.append(node)

    for del_mat in set(del_mat_list):
        try:
            print 'delete ' + str(del_mat)
            cmds.delete(del_mat)
        except:
            continue
    
def RedshifttoAnorld(self):
    
    StartShader = 'RedshiftMaterial'
    EndShader = 'aiStandardSurface'
    
    
    diff_color1 = '.diffuse_color'
    diff_color2 = '.baseColor'
    
    metalness1 = '.refl_metalness'
    metalness2 = '.metalness'
    
    spc_w_parm1 = '.refl_weight'
    spc_w_parm2 = '.specular'
    
    spc_color1 = '.refl_color'
    spc_color2 = '.specularColor'
    
    spc_Roughness1 = '.refl_roughness'
    spc_Roughness2 = '.specularRoughness'
    
    tran_color1 = '.opacity_color'
    tran_color2 = '.opacity'
    
    bump_color1 = '.bump_input'
    bump_color2 = '.normalCamera'
    
    ai_list = cmds.ls(sl = True,type = StartShader)
    
    del_mat_list = []
    del_Displace_Utility_list = []
    
    for node in ai_list:
        new_shader = cmds.shadingNode(EndShader,n='ai'+'_'+ str(node) , asShader=True)
        old_shadingEngine = cmds.listConnections( node + '.outColor')
        for shading_node in old_shadingEngine:
            cmds.connectAttr(str(new_shader) + '.outColor' , str(shading_node) + '.surfaceShader',force=True)
            Displace_Utility = cmds.listConnections( shading_node + '.displacementShader')
            if ( Displace_Utility != None ):
                new_Displace_Utility = cmds.shadingNode('displacementShader',n='new_Dis_' + str(Displace_Utility[0]) , asShader=True)
                cmds.setAttr(str(new_Displace_Utility) + '.scale' , 0.1)
                Displace_tex_file = cmds.listConnections( Displace_Utility[0] + '.texMap')
                for Displace_tex_file_node in Displace_tex_file:
                    Displace_tex_file_node_type = cmds.nodeType(Displace_tex_file_node)
                    if(Displace_tex_file_node_type == 'file'):
                        cmds.connectAttr(str(Displace_tex_file_node) + '.outAlpha' , str(new_Displace_Utility) + '.displacement' , force=True)
                        cmds.connectAttr(str(new_Displace_Utility) + '.displacement' , shading_node + '.displacementShader' , force=True)
                        
                del_Displace_Utility_list.append(Displace_Utility[0])

        
        #diffuse_color
        diff_c_file = cmds.listConnections( node + diff_color1)
        diff_c_file_type = cmds.nodeType(diff_c_file)
        if ( diff_c_file != None and str(diff_c_file_type) == 'file' ):
            cmds.connectAttr(str(diff_c_file[0]) + '.outColor' , str(new_shader) + diff_color2 , force=True)
        else:  
            diff_c_number = cmds.getAttr(node+diff_color1)
            cmds.setAttr(new_shader + diff_color2 , diff_c_number[0][0],diff_c_number[0][1],diff_c_number[0][2],type="double3")
    
        #metalness_weight
        metalness_w_file = cmds.listConnections( node + metalness1)
        metalness_w_file_type = cmds.nodeType(metalness_w_file)
        if ( metalness_w_file != None and str(metalness_w_file_type) == 'file' ):
            #cmds.setAttr(new_shader + '.refl_fresnel_mode' , 2)
            cmds.connectAttr(str(metalness_w_file[0]) + '.outAlpha' , str(new_shader) + metalness2 , force=True)
        else:  
            metalness_w_number = cmds.getAttr(node+metalness1)
            cmds.setAttr(new_shader + metalness2 , metalness_w_number)
    
        
        #specular_weight
        spc_w_file = cmds.listConnections( node + spc_w_parm1)
        spc_w_file_type = cmds.nodeType(spc_w_file)
        if ( spc_w_file != None and str(spc_w_file_type) == 'file' ):
            cmds.connectAttr(str(spc_w_file[0]) + '.outAlpha' , str(new_shader) + spc_w_parm2 , force=True)
        else:  
            spc_w_number = cmds.getAttr(node+spc_w_parm1)
            cmds.setAttr(new_shader + spc_w_parm2 , spc_w_number)
        
        #specular_color
        spc_c_file = cmds.listConnections( node + spc_color1)
        spc_c_file_type = cmds.nodeType(spc_c_file)
        if ( spc_c_file != None and str(spc_c_file_type) == 'file'  ):
            cmds.connectAttr(str(spc_c_file[0]) + '.outColor' , str(new_shader) + spc_color2 , force=True)
        else:  
            spc_c_number = cmds.getAttr(node+spc_color1)
            cmds.setAttr(new_shader + spc_color2 , spc_c_number[0][0],spc_c_number[0][1],spc_c_number[0][2],type="double3")
       
        #specularRoughness
        spcrou_w_file = cmds.listConnections( node + spc_Roughness1)
        spcrou_w_file_type = cmds.nodeType(spcrou_w_file)
        if ( spcrou_w_file != None and str(spcrou_w_file_type) == 'file' ):
            cmds.connectAttr(str(spcrou_w_file[0]) + '.outAlpha' , str(new_shader) + spc_Roughness2 , force=True)
        else:  
            spcrou_w_number = cmds.getAttr(node+spc_Roughness1)
            cmds.setAttr(new_shader + spc_Roughness2 , spcrou_w_number)
        
        #opacity_color
        tran_c_file = cmds.listConnections( node + tran_color1)
        tran_c_file_type = cmds.nodeType(tran_c_file)
        if ( tran_c_file != None and str(tran_c_file_type) == 'file' ):
            cmds.connectAttr(str(tran_c_file[0]) + '.outColor' , str(new_shader) + tran_color2 , force=True)
        else:  
            tran_c_number = cmds.getAttr(node+tran_color1)
            cmds.setAttr(new_shader + tran_color2 , int(tran_c_number[0][0]),int(tran_c_number[0][1]),int(tran_c_number[0][2]),type="double3")  
        
        #normal_bump
        ainormap = cmds.listConnections( node + bump_color1)
        if ( ainormap != None ):
            ainormap_type = cmds.nodeType(ainormap[0])
            if(ainormap_type == 'RedshiftBumpMap'):
                ainormap_file = cmds.listConnections( ainormap[0] + '.input')
                new_bump_node = cmds.shadingNode('aiNormalMap',n='new_aibump_' + str(ainormap_file[0]) , asTexture=True)
                cmds.setAttr(str(ainormap_file[0]) + '.alphaIsLuminance' , 1)
                #cmds.setAttr(str(new_bump_node) + '.colorToSigned' , 0)
                cmds.setAttr(str(new_bump_node) + '.strength' , 0.1)
                cmds.connectAttr(str(ainormap_file[0]) + '.outColor' , str(new_bump_node) + '.input' , force=True)
                cmds.connectAttr(str(new_bump_node) + '.outValue' , str(new_shader) + bump_color2 , force=True)
                cmds.delete(ainormap[0])
            if(ainormap_type == 'bump2d'):
                ainormap_file = cmds.listConnections( ainormap[0] + '.bumpValue')
                new_bump_node = cmds.shadingNode('aiNormalMap',n='new_aibump_' + str(ainormap_file[0]) , asTexture=True)
                cmds.setAttr(str(ainormap_file[0]) + '.alphaIsLuminance' , 1)
                cmds.setAttr(str(new_bump_node) + '.colorToSigned' , 0)
                cmds.connectAttr(str(ainormap_file[0]) + '.outColor' , str(new_bump_node) + '.input' , force=True)
                cmds.connectAttr(str(new_bump_node) + '.outValue' , str(new_shader) + bump_color2 , force=True)
                cmds.delete(ainormap[0])
        
        
        
        
        del_mat_list.append(node)
        
    for del_mat in set(del_mat_list):
        try:
            print 'delete ' + str(del_mat)
            cmds.delete(del_mat)
        except:
            continue
    for del_Displace_Utility in set(del_Displace_Utility_list):
        try:
            print 'delete ' + str(del_Displace_Utility)
            cmds.delete(del_Displace_Utility)
        except:
            continue
    

    

def AnolrdtoHoudiniBlinn(self):

    StartShader = 'aiStandardSurface'
    EndShader = 'blinn'
    
    
    diff_color1 = '.baseColor'
    diff_color2 = '.color'
    
    metalness1 = '.metalness'
    metalness2 = '.diffuse'
    
    
    opacity_color1 = '.opacity'
    opacity_color2 = '.ambientColor'
    
    spc_Roughness1 = '.specularRoughness'
    spc_Roughness2 = '.incandescence'
    
    
    bump_color1 = '.normalCamera'
    bump_color2 = '.normalCamera'
    
    transparency1 = '.subsurfaceColor'
    transparency2 = '.transparency'
    
    ai_list = cmds.ls(sl = True,type = StartShader)
    
    del_mat_list = []
    del_Displace_Utility_list = []
    
    for node in ai_list:
        new_shader = cmds.shadingNode(EndShader,n=EndShader+'_'+ str(node) , asShader=True)
        old_shadingEngine = cmds.listConnections( node + '.outColor')
        for shading_node in old_shadingEngine:
            cmds.connectAttr(str(new_shader) + '.outColor' , str(shading_node) + '.surfaceShader',force=True)
            Displace_Utility = cmds.listConnections( shading_node + '.displacementShader')
            if ( Displace_Utility != None ):
                if(cmds.nodeType(Displace_Utility) == 'displacementShader'):
                    Displace_tex_file = cmds.listConnections( Displace_Utility[0] + '.displacement')
                    for Displace_tex_file_node in Displace_tex_file:
                        Displace_tex_file_node_type = cmds.nodeType(Displace_tex_file_node)
                        if(Displace_tex_file_node_type == 'file'):
                            cmds.connectAttr(str(Displace_tex_file_node) + '.outColor' , str(new_shader) + '.specularColor' , force=True)
                if(cmds.nodeType(Displace_Utility) == 'file'):
                    cmds.connectAttr(str(Displace_Utility[0]) + '.outColor' , str(new_shader) + '.specularColor' , force=True)
    
                        
                del_Displace_Utility_list.append(Displace_Utility[0])
        #diffuse_color
        diff_c_file = cmds.listConnections( node + diff_color1)
        diff_c_file_type = cmds.nodeType(diff_c_file)
        if ( diff_c_file != None and str(diff_c_file_type) == 'file' ):
            cmds.connectAttr(str(diff_c_file[0]) + '.outColor' , str(new_shader) + diff_color2 , force=True)
        else:  
            diff_c_number = cmds.getAttr(node+diff_color1)
            cmds.setAttr(new_shader + diff_color2 , diff_c_number[0][0],diff_c_number[0][1],diff_c_number[0][2],type="double3")
            
        #metalness_weight
        metalness_w_file = cmds.listConnections( node + metalness1)
        metalness_w_file_type = cmds.nodeType(metalness_w_file)
        if ( metalness_w_file != None and str(metalness_w_file_type) == 'file' ):
            cmds.connectAttr(str(metalness_w_file[0]) + '.outAlpha' , str(new_shader) + metalness2 , force=True)
        else:  
            metalness_w_number = cmds.getAttr(node+metalness1)
            cmds.setAttr(new_shader + metalness2 , metalness_w_number)
         
        #opacity_color
        opa_c_file = cmds.listConnections( node + opacity_color1)
        opa_c_file_type = cmds.nodeType(opa_c_file)
        if ( opa_c_file != None and str(opa_c_file_type) == 'file'  ):
            cmds.connectAttr(str(opa_c_file[0]) + '.outColor' , str(new_shader) + opacity_color2 , force=True)
        else:  
            opa_c_number = cmds.getAttr(node+opacity_color1)
            cmds.setAttr(new_shader + opacity_color2 , opa_c_number[0][0],opa_c_number[0][1],opa_c_number[0][2],type="double3")
    
        #transparency_color
        
        transparency_c_file = cmds.listConnections( node + transparency1)
        transparency_c_file_type = cmds.nodeType(transparency_c_file)
        if ( transparency_c_file != None and str(transparency_c_file_type) == 'file'  ):
            cmds.connectAttr(str(transparency_c_file[0]) + '.outColor' , str(new_shader) + transparency2 , force=True)
        else:  
            transparency_c_number = cmds.getAttr(node+transparency1)
            cmds.setAttr(new_shader + transparency2 , transparency_c_number[0][0],transparency_c_number[0][1],transparency_c_number[0][2],type="double3")
         
        #specularRoughness
        spcrou_w_file = cmds.listConnections( node + spc_Roughness1)
        spcrou_w_file_type = cmds.nodeType(spcrou_w_file)
        if ( spcrou_w_file != None and str(spcrou_w_file_type) == 'file' ):
            cmds.connectAttr(str(spcrou_w_file[0]) + '.outColor' , str(new_shader) + spc_Roughness2 , force=True)
        if ( spcrou_w_file != None and str(spcrou_w_file_type) == 'aiRange' ):
            spcrou_w_file2 = cmds.listConnections( spcrou_w_file[0] + '.input')
            cmds.connectAttr(str(spcrou_w_file2[0]) + '.outColor' , str(new_shader) + spc_Roughness2, force=True)
            
        if ( spcrou_w_file == None):  
            spcrou_w_number = cmds.getAttr(node+spc_Roughness1)
            cmds.setAttr(new_shader + spc_Roughness2 , spcrou_w_number,spcrou_w_number,spcrou_w_number,type="double3")
        
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
        #del_mat_list.append(node)

       
    
    
if cmds.window('maya_material_convert_tools',ex=True):
    cmds.deleteUI('maya_material_convert_tools',wnd=True)

cmds.window('maya_material_convert_tools',t='maya_material_convert_tools',widthHeight=(400, 500))
cmds.columnLayout(adj=True)
cmds.text(l='arnold to redshift(PBR_metalness):',align='left',fn = 'boldLabelFont')
cmds.button(l='select_AnorldMaterials',c=select_Anorld)
cmds.button(l='AnorldToRedshift_PBR_metalness',c=AnorldToRedshift)
cmds.text(l='redshift to arnold(PBR_metalness):',align='left',fn = 'boldLabelFont')
cmds.button(l='select_RedshiftMaterials',c=select_Redshift)
cmds.button(l='RedshiftToAnorld_PBR_metalness',c=RedshifttoAnorld)
cmds.text(l='arnold to blinn:',align='left',fn = 'boldLabelFont')
cmds.button(l='select_AnorldMaterials',c=select_Anorld)
cmds.button(l='AnorldToBlinn(traditional)',c=AnorldToBlinn)
cmds.text(l='redshift to blinn:',align='left',fn = 'boldLabelFont')
cmds.button(l='to arnold then to blinn? :)')
cmds.text(l='Arnold To Houdini_blinn:',align='left',fn = 'boldLabelFont')
cmds.button(l='ArnoldToHoudini_blinn',c=AnolrdtoHoudiniBlinn)
cmds.text(l='about:',align='left',fn = 'boldLabelFont')
cmds.button(l='update_and_help',c=open_help)
cmds.showWindow()