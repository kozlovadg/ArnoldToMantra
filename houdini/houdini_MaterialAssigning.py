# SET_MATERIAL

s@base_color_tex = chs("parm") + s@material + "/" + s@material + "_%(UDIM)d.baseColor._acescg.exr.rat";
s@normal_tex = chs("parm") + s@material + "/" + s@material + "_%(UDIM)d.normalCamera._raw.exr.rat";
s@specular_color_tex = chs("parm") + s@material + "/" + s@material + "_%(UDIM)d.specularColor._acescg.exr.rat";
s@specular_roughness_tex = chs("parm") + s@material + "/"  + s@material + "_%(UDIM)d.specularRoughness._raw.exr.rat";
s@specular_ior_tex = chs("parm") + s@material + "/"  + s@material + "_%(UDIM)d.specularIOR._raw.exr.rat";
s@metalness_arnold_tex = chs("parm") + s@material + "/" + s@material + "_%(UDIM)d.metalness._raw.exr.rat";




# TEX_EXIST_CHECK

import os

node = hou.pwd()
geo = node.geometry()

node = hou.pwd()
geo = node.geometry()
prims = geo.prims()

geo.addAttrib(hou.attribType.Prim, "base_color_tex_exists", 1)
geo.addAttrib(hou.attribType.Prim, "metalness_tex_exists", 1)
geo.addAttrib(hou.attribType.Prim, "normal_tex_exists", 1)
geo.addAttrib(hou.attribType.Prim, "specular_color_tex_exists", 1)
geo.addAttrib(hou.attribType.Prim, "specular_roughness_tex_exists", 1)
geo.addAttrib(hou.attribType.Prim, "specular_ior_tex_exists", 1)

for prim in prims:
    tex = prim.attribValue('base_color_tex').replace("%(UDIM)d", '1001')
    prim.setAttribValue("base_color_tex_exists", os.path.isfile(tex))
    
    tex = prim.attribValue('metalness_arnold_tex').replace("%(UDIM)d", '1001')
    prim.setAttribValue("metalness_tex_exists", os.path.isfile(tex))
    
    tex = prim.attribValue('normal_tex').replace("%(UDIM)d", '1001')
    prim.setAttribValue("normal_tex_exists", os.path.isfile(tex))
    
    tex = prim.attribValue('specular_color_tex').replace("%(UDIM)d", '1001')
    prim.setAttribValue("specular_color_tex_exists", os.path.isfile(tex))
    
    tex = prim.attribValue('specular_roughness_tex').replace("%(UDIM)d", '1001')
    prim.setAttribValue("specular_roughness_tex_exists", os.path.isfile(tex))
    
    tex = prim.attribValue('specular_ior_tex').replace("%(UDIM)d", '1001')
    prim.setAttribValue("specular_ior_tex_exists", os.path.isfile(tex))



# ARNOLD_ATTRIBUTES

import hou
import os
import re

node = hou.pwd()
geo = node.geometry()
prims = geo.prims()

geo.addAttrib(hou.attribType.Prim, "base", 1.0)
geo.addAttrib(hou.attribType.Prim, "base_color", (1.0, 1.0, 1.0))
geo.addAttrib(hou.attribType.Prim, "diffuseRoughness", 1.0)
geo.addAttrib(hou.attribType.Prim, "specular", 1.0)
geo.addAttrib(hou.attribType.Prim, "specular_color", (1.0, 1.0, 1.0))
geo.addAttrib(hou.attribType.Prim, "specular_roughness", 1.0)
geo.addAttrib(hou.attribType.Prim, "specular_ior", 1.0)
geo.addAttrib(hou.attribType.Prim, "specularAnisotropy", 1.0)
geo.addAttrib(hou.attribType.Prim, "specularRotation", 1.0)
geo.addAttrib(hou.attribType.Prim, "metalness_arnold", 1.0)
geo.addAttrib(hou.attribType.Prim, "transmission", 1.0)
geo.addAttrib(hou.attribType.Prim, "transmissionColor", (1.0, 1.0, 1.0))
geo.addAttrib(hou.attribType.Prim, "transmissionDepth", 1.0)
geo.addAttrib(hou.attribType.Prim, "transmissionDispersion", 1.0)
geo.addAttrib(hou.attribType.Prim, "coat", 1.0)
geo.addAttrib(hou.attribType.Prim, "coatColor", (1.0, 1.0, 1.0))
geo.addAttrib(hou.attribType.Prim, "coatRoughness", 1.0)
geo.addAttrib(hou.attribType.Prim, "coatIOR", 1.0)
geo.addAttrib(hou.attribType.Prim, "opacity", 1.0)

parentFolder = '/cg/projects/virtus/assets/robots/scenes/ipolice_a/texturing/wip/v06/'

for i in os.listdir(parentFolder):
    for j in os.listdir(os.path.join(parentFolder, i)):
        if j.endswith("txt"):
            fileFromArnold = open(os.path.join(os.path.join(parentFolder, i), j), 'r')
            with fileFromArnold as searchfile:
                for line in searchfile:
                
                    if 'base ' in line:
                        base = float(re.findall("\d+\.\d+", line)[0])
                    
                    if 'baseColor ' in line:
                        baseColorStr = re.findall("\d+\.\d+", line)
                        baseColor = []
                        for str in baseColorStr:
                            baseColor.append(float(str))
                        baseColor = tuple(baseColor)
                        
                    if 'diffuseRoughness ' in line:
                        diffuseRoughness = float(re.findall("\d+\.\d+", line)[0])
                        
                    if 'specular ' in line:
                        specular = float(re.findall("\d+\.\d+", line)[0])
                        
                    if 'specularColor ' in line:
                        specularColorStr = re.findall("\d+\.\d+", line)
                        specularColor = []
                        for str in specularColorStr:
                            specularColor.append(float(str))
                        specularColor = tuple(specularColor)
                        
                    if 'specularRoughness ' in line:
                        specularRoughness = float(re.findall("\d+\.\d+", line)[0])
                        
                    if 'specularIOR ' in line:
                        specularIOR = float(re.findall("\d+\.\d+", line)[0])
                        
                    if 'specularAnisotropy ' in line:
                        specularAnisotropy = float(re.findall("\d+\.\d+", line)[0])
                        
                    if 'specularRotation ' in line:
                        specularRotation = float(re.findall("\d+\.\d+", line)[0])

                    if 'metalness ' in line:
                        metalness = float(re.findall("\d+\.\d+", line)[0])    
                        
                    if 'transmission ' in line:
                        transmission = float(re.findall("\d+\.\d+", line)[0]) 
                        
                    if 'transmissionColor ' in line:
                        transmissionColorStr = re.findall("\d+\.\d+", line)
                        transmissionColor = []
                        for str in transmissionColorStr:
                            transmissionColor.append(float(str))
                        transmissionColor = tuple(transmissionColor)
                    
                    if 'transmissionDepth ' in line:
                        transmissionDepth = float(re.findall("\d+\.\d+", line)[0])
                        
                    if 'transmissionDispersion ' in line:
                        transmissionDispersion = float(re.findall("\d+\.\d+", line)[0])
                        
                    if 'coat ' in line:
                        coat = float(re.findall("\d+\.\d+", line)[0])
                        
                    if 'coatColor ' in line:
                        coatColorStr = re.findall("\d+\.\d+", line)
                        coatColor = []
                        for str in coatColorStr:
                            coatColor.append(float(str))
                        coatColor = tuple(coatColor)
                        
                    if 'coatRoughness ' in line:
                        coatRoughness = float(re.findall("\d+\.\d+", line)[0])
                        
                    if 'coatIOR ' in line:
                        coatIOR = float(re.findall("\d+\.\d+", line)[0])
                        
                    if 'opacity ' in line:
                        opacity = float(re.findall("\d+\.\d+", line)[0])
                        
            fileFromArnold.close()
            
            for prim in prims:
                if prim.attribValue('material') == i:
                    
                    prim.setAttribValue('base', base) 
                    prim.setAttribValue('base_color', baseColor)
                    prim.setAttribValue('diffuseRoughness', diffuseRoughness)                   
                    prim.setAttribValue('specular', specular)                    
                    prim.setAttribValue('specular_color', specularColor)
                    prim.setAttribValue('specular_roughness', specularRoughness) 
                    prim.setAttribValue('specular_ior', specularIOR)
                    prim.setAttribValue('specularAnisotropy', specularAnisotropy)
                    prim.setAttribValue('specularRotation', specularRotation)
                    prim.setAttribValue('metalness_arnold', metalness)
                    prim.setAttribValue('transmission', transmission)
                    prim.setAttribValue('transmissionColor', transmissionColor)
                    prim.setAttribValue('transmissionDepth', transmissionDepth)
                    prim.setAttribValue('transmissionDispersion', transmissionDispersion)
                    prim.setAttribValue('coat', coat)
                    prim.setAttribValue('coatColor', coatColor)
                    prim.setAttribValue('coatRoughness', coatRoughness)
                    prim.setAttribValue('coatIOR', coatIOR)
                    prim.setAttribValue('opacity', opacity)
                    
            break
