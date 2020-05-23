import hou
import toolutils

shop_mat = hou.selectedNodes()

for node in shop_mat:
    a = '\$HIP/tex/' + node.parm('basecolor_texture').eval().split('/')[-1]
    node.parm('basecolor_texture').set(str(a))