def RedshifttoAnorld():
    import maya.cmds as cmds
    
    StartShader = 'RedshiftMaterial'
    EndShader = 'aiStandardSurface'
    
    
    diff_color1 = '.diffuse_color'
    diff_color2 = '.baseColor'

    emission_w1 = '.emission_weight'
    emission_w2 = '.emission'

    emission_color1 = '.emission_color'
    emission_color2 = '.emissionColor'

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
            
            
            
            
        #emission_weight
        emission_w_file = cmds.listConnections( node + emission_w1)
        if ( emission_w_file != None and str(cmds.nodeType(emission_w_file)) == 'file' ):
            cmds.connectAttr(str(emission_w_file[0]) + '.outAlpha' , str(new_shader) + emission_w2 , force=True)
        else:  
            cmds.setAttr(new_shader + emission_w2 , cmds.getAttr(node+emission_w1))
            
            
            
            
        #emission_color
        emission_c_file = cmds.listConnections( node + emission_color1)
        if ( emission_c_file != None and str(cmds.nodeType(emission_c_file)) == 'file' ):
            cmds.connectAttr(str(emission_c_file[0]) + '.outColor' , str(new_shader) + emission_color2 , force=True)
        else:  
            emission_c_number = cmds.getAttr(node+emission_color1)
            cmds.setAttr(new_shader + emission_color2 , emission_c_number[0][0],emission_c_number[0][1],emission_c_number[0][2],type="double3")
    

            
            
            
    
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
            
            
RedshifttoAnorld()