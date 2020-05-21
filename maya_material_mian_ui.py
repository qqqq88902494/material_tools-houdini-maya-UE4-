import maya.cmds as cmds
import webbrowser 
import AnolrdtoHoudiniBlinn
import AnorldToBlinn
import AnorldToRedshift
import RedshifttoAnorld

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


if cmds.window('maya_material_convert_tools',ex=True):
    cmds.deleteUI('maya_material_convert_tools',wnd=True)

cmds.window('maya_material_convert_tools',t='maya_material_convert_tools',widthHeight=(400, 500))
cmds.columnLayout(adj=True)
cmds.text(l='arnold to redshift(PBR_metalness):',align='left',fn = 'boldLabelFont')
cmds.button(l='select_AnorldMaterials',c=select_Anorld)
cmds.button(l='AnorldToRedshift_PBR_metalness',c='AnorldToRedshift.AnorldToRedshift()')
cmds.text(l='redshift to arnold(PBR_metalness):',align='left',fn = 'boldLabelFont')
cmds.button(l='select_RedshiftMaterials',c=select_Redshift)
cmds.button(l='RedshiftToAnorld_PBR_metalness',c='RedshifttoAnorld.RedshifttoAnorld()')
cmds.text(l='arnold to blinn:',align='left',fn = 'boldLabelFont')
cmds.button(l='select_AnorldMaterials',c=select_Anorld)
cmds.button(l='AnorldToBlinn(traditional)',c='AnorldToBlinn.AnorldToBlinn()')
cmds.text(l='redshift to blinn:',align='left',fn = 'boldLabelFont')
cmds.button(l='to arnold then to blinn? :)')
cmds.text(l='Arnold To Houdini_blinn:',align='left',fn = 'boldLabelFont')
cmds.button(l='ArnoldToHoudini_blinn',c='AnolrdtoHoudiniBlinn.AnolrdtoHoudiniBlinn()')
cmds.text(l='about:',align='left',fn = 'boldLabelFont')
cmds.button(l='update_and_help',c=open_help)
cmds.showWindow()