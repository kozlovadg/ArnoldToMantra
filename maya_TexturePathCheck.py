import maya.cmds as mc
import os
import shutil


def pathRemapTextures(new_tex_path=''):
    if len(new_tex_path) == 0:
        new_tex_path = mc.fileDialog2(fm=2, okc='Ok', cc='Cancel')[0]
    print new_tex_path

    textures_list = {}

    for root, dirs, files in os.walk(new_tex_path):
        for name in files:
            textures_list[name] = os.path.join(root, name)

    file_nodes = mc.ls(sl=True, type='file')
    if len(file_nodes) == 0:
        file_nodes = mc.ls(type='file')

    for obj in file_nodes:
        for attr in ['fileTextureName']:  # , 'fileTextureNamePattern', 'computedFileTextureNamePattern']:
            attr_path = '%s.%s' % (obj, attr)
            if maya.cmds.getAttr(attr_path, typ=True) == 'string':
                attr_value = maya.cmds.getAttr(attr_path)
                if len(attr_value) > 0:
                    print '\t old', attr_path, attr_value
                    if textures_list.has_key(os.path.basename(attr_value)):
                        print '\t new', textures_list[os.path.basename(attr_value)]
                        mc.setAttr(attr_path, str(textures_list[os.path.basename(attr_value)]), type="string")
                    else:
                        print 'WARNING! Missing file reference %s in %s'%(attr_value, obj)


                    
pathRemapTextures()
