import hou

shop = hou.node('/obj/')
listofNode = []
listofNode_map_difuse = []
listofNode_map_metalness = []
listofNode_map_spec = []
listofNode_map_specRoughness = []
listofNode_map_normal = []
listofNode_map_displacement = []

for child in shop.allSubChildren():
    if child.type().name() == "v_fbx":
        listofNode_map_difuse.append(child.parm("map1").eval())
        listofNode_map_metalness.append(child.parm("map2").eval())
        listofNode_map_specRoughness.append(child.parm("map3").eval())
        listofNode_map_spec.append(child.parm("map4").eval())
        listofNode_map_displacement.append(child.parm("map5").eval())
        listofNode_map_normal.append(child.parm("map6").eval())
    if child.type().name() == "material" and child.type().description() == "Subnetwork":
        listofNode.append(child.name())


#for child in shop.allSubChildren():
    #if child.type().name() == "shopnet":
        #shopnet = child

shopnet = hou.node('/mat/')
a = -1
num = len(listofNode)
for i in range(num):
    a += 1
    if len(listofNode_map_difuse[a]) != 0:
        mat_node = shopnet.createNode('principledshader::2.0', node_name=listofNode[a])
        mat_node.parm('basecolor_useTexture').set(1)
        mat_node.parm('basecolor_texture').set(listofNode_map_difuse[a])
        mat_node.parm('metallic_useTexture').set(1)
        mat_node.parm('metallic_texture').set(listofNode_map_metalness[a])
        mat_node.parm('reflect_useTexture').set(1)
        mat_node.parm('reflect_texture').set(listofNode_map_spec[a])
        mat_node.parm('rough_useTexture').set(1)
        mat_node.parm('rough_texture').set(listofNode_map_specRoughness[a])
        mat_node.parm('baseBumpAndNormal_enable').set(1)
        mat_node.parm('baseNormal_texture').set(listofNode_map_normal[a])
        mat_node.parm('dispTex_enable').set(1)
        mat_node.parm('dispTex_texture').set(listofNode_map_displacement[a])
    else:
        mat_node = mat_net.createNode('principledshader::2.0', node_name=listofNode[a])
# use Alt + w to remove old prefix at :rs_
