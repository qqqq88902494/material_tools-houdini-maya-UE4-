import os
import hou
f = open(r'C:\temp\txt\test.txt','r')  
lines = f.readlines() 
mat_shop = hou.node('/mat/')

for line in lines:
    if('-num-' in str(line)):
        node_name =  line.split('-num-')[0]
        num =  line.split('-num-')[1][:-1][1:-1]
        num_sub = num.split(', ')
        mat_node = mat_shop.createNode('principledshader::2.0', node_name=node_name)
        mat_node.parm('basecolorr').set(num_sub[0])
        mat_node.parm('basecolorg').set(num_sub[1])
        mat_node.parm('basecolorb').set(num_sub[2])
        mat_node.parm('reflect').set(0)
        #print num_sub
    if('-tex-' in str(line)):
        node_name =  line.split('-tex-')[0]
        tex_file =  line.split('-tex-')[1][:-1]
        #print tex_file
        mat_node = mat_shop.createNode('principledshader::2.0', node_name=node_name)
        mat_node.parm('basecolorr').set(0.8)
        mat_node.parm('basecolorg').set(0.8)
        mat_node.parm('basecolorb').set(0.8)
        mat_node.parm('reflect').set(0)
        mat_node.parm('basecolor_useTexture').set(1)
        mat_node.parm('basecolor_texture').set(tex_file)
        