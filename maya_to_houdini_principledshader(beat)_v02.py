# -*- coding: utf-8 -*-

import hou
import webbrowser
import toolutils
from PySide2 import QtCore, QtUiTools, QtWidgets

class Ui_Fbx_tools(QtWidgets.QMainWindow):
    def setupUi(self, Fbx_tools):
        Fbx_tools.setObjectName("Fbx_tools")
        Fbx_tools.resize(320, 200)
        Fbx_tools.setMinimumSize(QtCore.QSize(320, 200))
        Fbx_tools.setMaximumSize(QtCore.QSize(320, 200))
        self.convert_fbx = QtWidgets.QPushButton(Fbx_tools)
        self.convert_fbx.setGeometry(QtCore.QRect(60, 60, 201, 51))
        self.convert_fbx.setObjectName("convert_fbx")
        self.tipstxt = QtWidgets.QLabel(Fbx_tools)
        self.tipstxt.setGeometry(QtCore.QRect(0, 0, 311, 41))
        self.tipstxt.setObjectName("tipstxt")
        self.about = QtWidgets.QPushButton(Fbx_tools)
        self.about.setGeometry(QtCore.QRect(100, 130, 111, 41))
        self.about.setObjectName("about")

        self.retranslateUi(Fbx_tools)
        QtCore.QMetaObject.connectSlotsByName(Fbx_tools)        

        
        self.convert_fbx.clicked.connect(self.buttonClicked)
        self.about.clicked.connect(self.open_help)

        
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        

        
        self.setStyleSheet(hou.qt.styleSheet())
        self.setProperty("houdiniStyle", True)
        
    def retranslateUi(self, Fbx_tools):
    
        _translate = QtCore.QCoreApplication.translate
        Fbx_tools.setWindowTitle(_translate("Fbx_tools", "Fbx_tools"))
        self.convert_fbx.setText(_translate("Fbx_tools", "convert_fbx"))
        self.tipstxt.setText(_translate("Fbx_tools", "<html><head/><body><p><span style=\" font-size:11pt;\">Tips:Select the FbxSubnetWork you want to build</span></p></body></html>"))
        self.about.setText(_translate("Fbx_tools", "about"))
        
    def buttonClicked(self):

        
        listofNode = []
        listofNode_map = []
        fbxlistofNode = []
        
        fbx_selected_nodes = hou.selectedNodes()
        
        mat_shop = hou.node('/mat/')
        
        for fbx_sel_node in fbx_selected_nodes:
            fbx_mat_list_search = fbx_sel_node.allSubChildren()
            for fbx_mat_list in fbx_mat_list_search:
                if fbx_mat_list.type().name() == "material" and fbx_mat_list.type().description() == "Subnetwork":
                        for fbxshader in fbx_mat_list.allSubChildren():
                            if fbxshader.type().name() == "v_fbx":
                                listofNode_map.append(fbxshader.parm("map1").eval())
                                listofNode_map.append(fbxshader.parm("map2").eval())
                                listofNode_map.append(fbxshader.parm("map3").eval())
                                listofNode_map.append(fbxshader.parm("map4").eval())
                                listofNode_map.append(fbxshader.parm("map5").eval())
                                listofNode_map.append(fbxshader.parm("map6").eval())
                                listofNode.append(fbx_mat_list.name())
                                listofNode.append(listofNode_map)
                                
                                mat_node = mat_shop.createNode('principledshader::2.0', node_name=listofNode[0])
                                print 'create '+listofNode[0]+' in /mat/'
                                mat_node.parm('basecolorr').set(0.8)
                                mat_node.parm('basecolorg').set(0.8)
                                mat_node.parm('basecolorb').set(0.8)
                                mat_node.parm('baseNormal_scale').set(0.1)
                                mat_node.parm('dispTex_scale').set(1)
                                mat_node.parm('rough').set(1)
                                for tex_file in listofNode[1]:
                                    if('Albedo' in str(tex_file)):
                                        mat_node.parm('basecolor_useTexture').set(1)
                                        mat_node.parm('basecolor_texture').set(tex_file)
                                    if('Metalness' in str(tex_file)):
                                        mat_node.parm('metallic_useTexture').set(1)
                                        mat_node.parm('metallic_texture').set(tex_file)
                                    if('Displacement' in str(tex_file)):
                                        mat_node.parm('dispTex_enable').set(1)
                                        mat_node.parm('dispTex_texture').set(tex_file)
                                    if('Normal' in str(tex_file)):
                                        mat_node.parm('baseBumpAndNormal_enable').set(1)
                                        mat_node.parm('baseNormal_texture').set(tex_file)
                                    if('Roughness' in str(tex_file)):
                                        mat_node.parm('rough_useTexture').set(1)
                                        mat_node.parm('rough_texture').set(tex_file)
                                    if('Opacity' in str(tex_file)):
                                        mat_node.parm('opaccolor_useTexture').set(1)
                                        mat_node.parm('opaccolor_texture').set(tex_file)
                                    if('Translucency' in str(tex_file)):
                                        mat_node.parm('ssscolor_useTexture').set(1)
                                        mat_node.parm('ssscolor_texture').set(tex_file)
                                
                                listofNode = []
                                listofNode_map = []
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
        
    def open_help(self):

        webbrowser.open_new_tab('https://github.com/qqqq88902494/maya_material_convert_tools')
        
class MyWidget(Ui_Fbx_tools,QtWidgets.QWidget):
    def __init__(self,parent=None):
        super(MyWidget,self).__init__(parent)
        self.setupUi(self)
        

widget = MyWidget()
widget.show()