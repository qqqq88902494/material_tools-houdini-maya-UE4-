def AnolrdtoHoudiniBlinn():
    import maya.cmds as cmds
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