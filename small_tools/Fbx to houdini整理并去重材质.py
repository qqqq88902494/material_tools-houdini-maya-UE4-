import hou
import toolutils

listofNode = []
listofNode_map = []
fbxlistofNode = []


fbx_selected_nodes = hou.selectedNodes()


for fbx_sel_node in fbx_selected_nodes:
    matrial_path = []
    tuple_mat = ()
    fbx_mat_list_search = fbx_sel_node.allSubChildren()
    for fbx_mat_list in fbx_mat_list_search:
        if fbx_mat_list.type().name() == "file" and fbx_mat_list.type().description() == "File":
            primlist = fbx_mat_list.geometry().prims()
            for prim in primlist:
                matrial_path.append(prim.attribValue("shop_materialpath"))
            matrial_path = list(set(matrial_path))
        if fbx_mat_list.type().name() == "matnet":
            old_mat_shop = fbx_mat_list
            
    true_materials = list(set(matrial_path))
    
    for new_mat in true_materials:
        print 'move ' + str(new_mat) +' in ' +str(fbx_sel_node.name()) + '_matnet'
        new_mat2 = hou.node(old_mat_shop.path()+'/'+ new_mat)
        tuple_mat = tuple_mat + (new_mat2,)
    
    pos = fbx_sel_node.position()
    new_mat_shop = hou.node('/obj/').createNode('matnet',node_name= str(fbx_sel_node.name()) + '_matnet')
    new_mat_shop.setPosition(pos)
    new_mat_shop.move([0,-2])
    hou.moveNodesTo(tuple_mat,new_mat_shop)  

print '####################################'
print '####material building complete######'
print '####################################'
for nodefbx in fbx_selected_nodes:
    for filechild in nodefbx.allSubChildren():
        if filechild.type().description() == "File":
            print 'merge ' + str(filechild) + ' building in Fbx_Geo'
            fbxlistofNode.append(filechild.path())
    nodefbx.setDisplayFlag(False)
    root = hou.node("/obj")
    nodeGeo = root.createNode("geo",str(nodefbx) + "_Fbx_Geo")
    pos = nodefbx.position()
    nodeGeo.setPosition(pos)
    nodeGeo.move([0,-1])

    mergeNode = nodeGeo.createNode('merge', 'mergeAll')
    for index in range(len(fbxlistofNode)):
        node = nodeGeo.createNode('object_merge',"Geo"+ str(index +1))
        node.parm('objpath1').set(fbxlistofNode[index])
        node.parm('xformtype').set(1)
        awNode = nodeGeo.createNode('attribwrangle','set_mat_path')
        awNode.setInput(0,node)
        awNode.parm('class').set(1)
        expression0 = "s@shop_materialpath = sprintf('/mat/'+@shop_materialpath);"
        awNode.parm('snippet').set(expression0)
        mergeNode.setInput(index,awNode)
       
    nodeGeo.layoutChildren()
    null = nodeGeo.createNode('null','FBX_OUT')
    null.setInput(0,mergeNode)
    macolo = hou.Color((0,1,0.5))
    null.setColor(macolo)
    pos_merge = mergeNode.position()
    null.setPosition(pos_merge)
    null.move([0,-1])
    null.setDisplayFlag(True)
    null.setRenderFlag(True)
    fbxlistofNode = []
print '####################################'
print '######fbx building complete#########'
print '####################################'