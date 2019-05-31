import pymel.core as pm
import os

import pymel.core as pm
import os

def mixBlendAndShader(listofBlends, shadingMixNode):
    alSurfaceMixed = []
    for i in shadingMixNode.listConnections():
       if i.nodeType() == 'alSurface':
           alSurfaceMixed.append(i)
    
    blendToReturn = []
    buf = 0
    
    if pm.connectionInfo(shadingMixNode.name() + '.mix', id = True):
        connectedMix = 1
        maskToMix = pm.listConnections(shadingMixNode.name() + '.mix', p=True)[0]
    else:
        connectedMix = 0
        toMixNum = pm.getAttr(shadingMixNode.name() + '.mix')
        
    for blendToMix in listofBlends:
            
        AOV_name = blendToMix.name().split('_')[1]
        
        outputBlend = blendToMix.name() + '.output'
        if pm.getAttr(outputBlend, typ = True) == "float3":
            # VECTOR
            name = 'blendColors_' + AOV_name + '_' + shadingMixNode.name() +'_AOVS'
            nodeBlend = pm.createNode( 'blendColors' , n=name)
            nodeBlendAttr = nodeBlend.name() + '.color1'
            nodeBlendAttrOut = nodeBlend.name() + '.output'
            
        else:
            # FLOAT
            name = 'blendTwoAttr_' + AOV_name + '_' + shadingMixNode.name() +'_AOVS'
            nodeBlend = pm.createNode( 'blendTwoAttr' , n=name)
            nodeBlendAttr = nodeBlend.name() + '.input[0]'
            nodeBlendAttrOut = nodeBlend.name() + '.output'
        
        pm.connectAttr(outputBlend, nodeBlendAttr)
                
        if pm.getAttr(shadingMixNode.name() + '.mix') == 0:
            if (not connectedMix):
                if pm.getAttr(outputBlend, typ = True) == "float3":
                    pm.setAttr(nodeBlend + '.blender', toMixNum)
                else:
                    pm.setAttr(nodeBlend + '.attributesBlender', toMixNum)
            else:  
                if pm.getAttr(outputBlend, typ = True) == "float3":
                    pm.connectAttr(maskToMix.name(), nodeBlend + '.blender')
                else:
                    pm.connectAttr(maskToMix.name(), nodeBlend + '.attributesBlender')
        blendToReturn.append(nodeBlend)
        
    for i in blendToReturn:
        pasName = i.name().split('_')[1]
        if pasName == 'baseColor':
            pasName = 'diffuseColor'
        NpasName = pasName.replace('specular', 'specular1')
        pasName = NpasName
        
        nodeAttr = alSurfaceMixed[0] + '.' + pasName
        if pm.listConnections(nodeAttr):
            plug = pm.listConnections(nodeAttr, p=True)[0]
            if plug.type() == 'float3':
                nodeBlendAttr = i + '.color2' 
            else:
                nodeBlendAttr = i + '.input[1]' 
                      
            pm.connectAttr(plug, nodeBlendAttr) 
        else:
            parm = pm.getAttr(nodeAttr)
            if type(parm).__name__ == 'float':
                nodeConst = pm.createNode( 'floatConstant')
                nodeConstAttr = nodeConst + '.inFloat'
                pm.setAttr(nodeConstAttr, parm)
                nodeConstAttr = nodeConst + '.outFloat'
                nodeBlendAttr = i + '.input[1]' 
                pm.connectAttr(nodeConstAttr, nodeBlendAttr) 
            else:
                nodeConst = pm.createNode( 'colorConstant')
                nodeConstAttr = nodeConst + '.inColor'
                pm.setAttr(nodeConstAttr, parm)
                nodeConstAttr = nodeConst + '.outColor'
                nodeBlendAttr = i + '.color2' 
                pm.connectAttr(nodeConstAttr, nodeBlendAttr)  
    return blendToReturn
                

def mixTwoShaders(shadingMixNode, alSurfaceMixed, folder_to_save):
    
    buf = 0
    
    blendToReturn = []
    
    if pm.connectionInfo(shadingMixNode.name() + '.mix', id = True):
        connectedMix = 1
        maskToMix = pm.listConnections(shadingMixNode.name() + '.mix', p=True)[0]
    else:
        connectedMix = 0
        toMixNum = pm.getAttr(shadingMixNode.name() + '.mix')
        
    for shaderToMix in alSurfaceMixed:
        
        print shaderToMix
        # add .txt file with information of parametrs in shader
        fileName = os.path.join(folder_to_save, shaderToMix.name() + '.txt')
        preferencesFile = open(fileName, 'w+')
        
        for i in pm.listAttr(shaderToMix):
            value = pm.getAttr(shaderToMix.name() + '.' + i)
            try:
                preferencesFile.write(i)
                preferencesFile.write(" " + str(value))
            except:
                pass
            preferencesFile.write("\n")
            
        preferencesFile.close()
        
        listConnected = pm.listConnections(shaderToMix, p=True, d=False)
        for plug in listConnected:
            if buf == 0:
                    
                AOV_name = plug.outputs(p=True)[0].name().split('.')[1]
                
                if AOV_name == 'diffuseColor':
                    AOV_name = 'baseColor'
                
                AOV_name = ''.join(i for i in AOV_name if not i.isdigit())
                    
                    
                if plug.type() == 'float3':
                    name = 'blendColors_' + AOV_name + '_' + shadingMixNode.name() +'_AOVS'
                    nodeBlend = pm.createNode( 'blendColors' , n=name)
                    nodeBlendAttr = nodeBlend.name() + '.color2'
                    nodeBlendAttrOut = nodeBlend.name() + '.output'

                    pm.connectAttr(plug, nodeBlendAttr)
                else:
                    aiUserData = pm.createNode( 'aiUserDataColor')

                    R = aiUserData.name() + '.defaultValueR'
                    G = aiUserData.name() + '.defaultValueG'
                    B = aiUserData.name() + '.defaultValueB'
                    
                    pm.connectAttr(plug, R)
                    pm.connectAttr(plug, G)
                    pm.connectAttr(plug, B)

                    plugUserData = aiUserData.name() + '.outColor'

                    name = 'blendColors_' + AOV_name + '_' + shadingMixNode.name() +'_AOVS'
                    nodeBlend = pm.createNode( 'blendColors' , n=name)
                    nodeBlendAttr = nodeBlend.name() + '.color2'
                    nodeBlendAttrOut = nodeBlend.name() + '.output'

                    pm.connectAttr(plugUserData, nodeBlendAttr)
                
                
                if pm.getAttr(shadingMixNode.name() + '.mix') == 0:
                    if (not connectedMix):
                        pm.setAttr(nodeBlend + '.blender', toMixNum)
                    else:  
                        pm.connectAttr(maskToMix.name(), nodeBlend + '.blender')

                
                blendToReturn.append(nodeBlend)
                
            elif (buf == 1):
                AOV_name = plug.outputs(p=True)[0].name().split('.')[1]
                
                if AOV_name == 'diffuseColor':
                    AOV_name = 'baseColor'
                
                AOV_name = ''.join(i for i in AOV_name if not i.isdigit())
                
                if not (pm.objExists('blendColors_' + AOV_name + '_' + shadingMixNode.name() +'_AOVS')):
                    
                    pass
                    
                    # ADD LATER
                else:
                    if plug.type() == 'float3':
                        nodeBlendAttr = 'blendColors_' + AOV_name + '_' + shadingMixNode.name() +'_AOVS' + '.color1' 

                        pm.connectAttr(plug, nodeBlendAttr) 
                    else:
                        aiUserData = pm.createNode( 'aiUserDataColor')

                        R = aiUserData.name() + '.defaultValueR'
                        G = aiUserData.name() + '.defaultValueG'
                        B = aiUserData.name() + '.defaultValueB'
                        
                        pm.connectAttr(plug, R)
                        pm.connectAttr(plug, G)
                        pm.connectAttr(plug, B)

                        plugUserData = aiUserData.name() + '.outColor'

                        nodeBlendAttr = 'blendColors_' + AOV_name + '_' + shadingMixNode.name() +'_AOVS' + '.color1'  

                        pm.connectAttr(plugUserData, nodeBlendAttr)

        buf += 1

    for blendNode in blendToReturn:
        nameBlendAttr = blendNode.name() + '.output'

        pasName = blendNode.name().split('_')[1]
        AOV_name = pasName

        nametotest = "aiAOV_" + AOV_name
        if not (nametotest in listOfAovsEnabled):
            print 'ERROR TO PASS ' + AOV_name
        else:
            pm.setAttr("aiAOV_" + AOV_name + ".enabled", 1)

        if pm.getAttr(nameBlendAttr, type=True) == 'float3':
            nameBlendAttr = blendNode.name() + '.color1'
            print nameBlendAttr, pm.listConnections(nameBlendAttr)
            if pm.listConnections(nameBlendAttr):
                pass
            else:

                if pasName == 'baseColor':
                    pasName = 'diffuseColor'
                NpasName = pasName.replace('specular', 'specular1')
                pasName = NpasName

                nodeAttr = alSurfaceMixed[1] + '.' + pasName

                parm = pm.getAttr(nodeAttr)

                if type(parm).__name__ == 'float':
                    parmN = (parm, parm, parm)
                    parm = parmN 

                nodeConst = pm.createNode( 'colorConstant')
                nodeConstAttr = nodeConst + '.inColor'
                pm.setAttr(nodeConstAttr, parm)
                nodeConstAttr = nodeConst + '.outColor'
                nodeBlendAttr = blendNode + '.color1' 
                #print nodeBlendAttr
                pm.connectAttr(nodeConstAttr, nodeBlendAttr)  
        else:
            pass

    return blendToReturn    
    
def createWriteNodes(shadingMixNode, shadingGroupNode, blendReturned):

    for i in blendReturned:
        attr = i + '.output'
        if pm.getAttr(attr, type=True) == 'float3':
            # VECTOR
            typeAttr = 'vector'
            nodeToConnect = pm.createNode( 'aiWriteColor' , n='aiWriteColor_AOV')
        else:
            # FLOAT
            typeAttr = 'float'
            nodeToConnect = pm.createNode( 'aiWriteFloat' , n='aiWriteFloat_AOV')
        AOV_name = i.name().split('_')[1]
        attrToConnect = nodeToConnect.listAttr(st='input')
                        
        attrName = nodeToConnect.listAttr(st='aovName')
        pm.setAttr(attrName[0], AOV_name)
        pm.connectAttr(attr, attrToConnect[0])

        inConnect = shadingGroupNode.listConnections(d=False, t=['alLayer', 'aiWriteColor', 'aiWriteFloat'], p=True)[0]
        pm.connectAttr(inConnect, nodeToConnect.listAttr(st='beauty')[0])
        pm.connectAttr(nodeToConnect.listAttr(st='outColor')[0], shadingGroupNode.listAttr(st='surfaceShader')[0], f=True)
    
    selectionList = []    
    for i in shadingGroupNode.listConnections():
        if i.nodeType() == "transform":
            selectionList.append(i)
    
    pm.select(selectionList)
            
    pm.showHidden()
    
    folder_to_save = os.path.join(folder_to_save_base, shadingMixNode.name())
       
    s = pm.ls(sl=True)
    nameTr = shadingMixNode.name()
    if (len(s) != 1):
        pm.polyUnite(s, n=nameTr)
    #cmds.arnoldRenderToTexture(folder=folder_to_save, enable_aovs=True, resolution=2048, all_udims=True)
    pm.select(cl=True)
                
def alLayer(shadingMixNode, shadingGroupNode, t, folder_to_save):

    if (not t):
        for i in shadingGroupNode.listConnections():
            if i.nodeType() == "transform":
                selectionList.append(i)
                
        # DISABLE ALL AOVS
        for aov in listOfAovsEnabled:
            pm.setAttr(aov + ".enabled", 0)
        
        
        # CREATE FOLDER TO SAVE (AOV)
        folder_to_save = os.path.join(folder_to_save_base, shadingMixNode.name())
        if not os.path.exists(folder_to_save):
            os.makedirs(folder_to_save)
            
        
    check = False        
    for j in shadingMixNode.listConnections(d=False):
        if j.nodeType()=='alLayer':
            listofBlends = alLayer(j, shadingGroupNode, 1, folder_to_save)
            check = True
    
    if check:
        name1 = shadingMixNode.name() + '.layer1'
        connectedToFirst = pm.listConnections(name1)[0]
        
        name2 = shadingMixNode.name() + '.layer2'
        connectedToSecond = pm.listConnections(name2)[0]
        
        first = False
        second = False
        for elem in listofBlends:
            if connectedToFirst.name() in elem.name():
                first = True
                break
        for elem in listofBlends:
            if connectedToSecond.name() in elem.name():
                second = True
                break
        
        if first and not second:
            blendReturned = mixBlendAndShader(listofBlends, shadingMixNode)
            return blendReturned
        
    if not check:
        alSurfaceMixed = []
        nameLayer = shadingMixNode.name() + '.layer1'
        i = pm.listConnections(nameLayer)[0]
        if i.nodeType() == 'alSurface':
           alSurfaceMixed.append(i)

        nameLayer = shadingMixNode.name() + '.layer2'
        i = pm.listConnections(nameLayer)[0]
        if i.nodeType() == 'alSurface':
           alSurfaceMixed.append(i)
        
        blendReturned = mixTwoShaders(shadingMixNode, alSurfaceMixed, folder_to_save)
        return blendReturned

listofAOVS = []

shader_nodes = pm.ls( type='shadingEngine')

allMesh = cmds.ls(type='mesh')
listOfAovsEnabled = ['aiAOV_baseColor', 'aiAOV_specularColor', 'aiAOV_specularRoughness', 'aiAOV_normalCamera', 'aiAOV_metalness', 'aiAOV_specularStrength', 'aiAOV_specularReflectivity']
folder_to_save_base = "/cg/projects/virtus/assets/robots/scenes/mark3/texturing/wip/v02/"

list = ['mark03_Exhaust_lc_ALayerSG']

# разобаоться с хайдами анхайдами и включением аовов (а еще тройной спекРефлекшн пасс втф)
for i in shader_nodes:
    cmds.hide(allMesh)  
    selectionList = []
    
    if i.name() in list:
      
        for l in i.listConnections(d=False):
            
            #if l.nodeType()=='alSurface':
            #    alSurface(l, i)
            
            if l.nodeType()=='alLayer':
                blendReturned = alLayer(l, i, 0, folder_to_save_base)
                createWriteNodes(l, i, blendReturned)

    

# FUNCTION PARSING AI SHADER NODES
def checkAiShaderSurface(shader_node, shadingGroupNode):

    for i in shadingGroupNode.listConnections():
        if i.nodeType() == "transform":
            selectionList.append(i)
      
          
    if selectionList:

        # DISABLE ALL AOVS
        for aov in listOfAovsEnabled:
            pm.setAttr(aov + ".enabled", 0)
        
        listConnected = pm.listConnections(shader_node, p=True, d=False)
        
        
        # CREATE FOLDER TO SAVE (AOV)
        folder_to_save = os.path.join(folder_to_save_base, shader_node.name())
        if not os.path.exists(folder_to_save):
            os.makedirs(folder_to_save)
            
            
        # add .txt file with information of parametrs in shader
        fileName = os.path.join(folder_to_save, shader_node.name() + '.txt')
        preferencesFile = open(fileName, 'w+')
        
        for i in pm.listAttr(shader_node):
            value = pm.getAttr(shader_node.name() + '.' + i)
            try:
                preferencesFile.write(i)
                preferencesFile.write(" " + str(value))
            except:
                pass
            preferencesFile.write("\n")
            
        preferencesFile.close()
        
        aovExistsV = shader_node.listConnections(s=False, t='aiWriteColor')
        aovExistsF = shader_node.listConnections(s=False, t='aiWriteFloat')
        
        if (len(aovExistsV)==0 and len(aovExistsF)==0):
            # DID NOT CREATE AOVS NODE
            
            for plug in listConnected:
                if "float3" in plug.type():
                    # VECTOR
                    typeAttr = 'vector'
                    nodeToConnect = pm.createNode( 'aiWriteColor' , n='aiWriteColor_AOV')
                    
                else:
                    # FLOAT
                    typeAttr = 'float'
                    nodeToConnect = pm.createNode( 'aiWriteFloat' , n='aiWriteFloat_AOV')
                
                attrToConnect = nodeToConnect.listAttr(st='input')
                    
                attrName = nodeToConnect.listAttr(st='aovName') 
                AOV_name = plug.outputs(p=True)[0].name().split('.')[1]
                pm.setAttr(attrName[0], AOV_name)
                
                if (typeAttr, AOV_name) not in listofAOVS:
                    listofAOVS.append((typeAttr, AOV_name))

                if (AOV_name != "inputs[7]"):
                    if (AOV_name != "layer2a"):
                        pm.setAttr("aiAOV_" + AOV_name + ".enabled", 1)
                    else:     
                        pass

                    
                pm.connectAttr(plug, attrToConnect[0])
        
            
                inConnect = shadingGroupNode.listConnections(d=False, t=['aiStandardSurface', 'aiWriteColor', 'aiWriteFloat'], p=True)[0]
                pm.connectAttr(inConnect, nodeToConnect.listAttr(st='beauty')[0])
                
                pm.connectAttr(nodeToConnect.listAttr(st='outColor')[0], shadingGroupNode.listAttr(st='surfaceShader')[0], f=True)
            
            pm.select(selectionList)
            
            pm.showHidden()
               
            s = pm.ls(sl=True)
            nameTr = shader_node.name()
            if shader_node.name() != "krissVector_black_part26_nl_shd_aiss":
                if (len(s) != 1):
                    pm.polyUnite(s, n=nameTr)
            cmds.arnoldRenderToTexture(folder=folder_to_save, enable_aovs=True, resolution=2048, all_udims=True)
            pm.select(cl=True)

        else:
            # ALREADY CREATED AOVS NODE
            print "BAKED WAS ALREADY DONE TO %s shader" % shader_node.name()

    else:
        print "NO OBJECTS ASSIGN TO %s shader" % shader_node.name()



# GLOBAL VARIABLES
listofAOVS = []
folder_to_save_base = "/cg/projects/virtus/assets/doubles/scenes/inner_suit_l1/texturing/wip/v02/"

listOfAovsEnabled = ['aiAOV_baseColor', 'aiAOV_metalness', 'aiAOV_normalCamera', 'aiAOV_opacityG', 'aiAOV_specularColor', 'aiAOV_specularIOR', 'aiAOV_specularRoughness', 'aiAOV_base', 'aiAOV_specular']

shader_nodes = pm.ls(sl=True, type='aiStandardSurface')
if len(shader_nodes) == 0:
    shader_nodes = pm.ls(type='aiStandardSurface')
    
allMesh = cmds.ls(type='mesh')

# MAIN LOOP THROUGHT ALL SHADERS    

for shader_node in shader_nodes:
    
    cmds.hide(allMesh)
    
    selectionList = []
    
    # PARSING TRANSFORM OF OBJECTS WITH MATERIAL
    try:
        shadingGroupNode = shader_node.listConnections(s=False, t='shadingEngine')[0]
        checkAiShaderSurface(shader_node, shadingGroupNode)
    except:
        checkMixShader(shader_node)

saveAndRename()    
        
print "FINISHED!"
