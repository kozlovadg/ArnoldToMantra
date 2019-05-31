parentFolder = '/cg/projects/virtus/assets/robots/scenes/ipolice_a/texturing/wip/v06/'

for i in os.listdir(parentFolder):
    for j in os.listdir(os.path.join(parentFolder, i)):
        if j.endswith("exr") and not j.endswith(".acescg.exr") :
            old = os.path.join(os.path.join(parentFolder, i), j)
            texture = os.path.join(os.path.join(path, i), j)
            read_node = nuke.nodes.Read()
            read_node['file'].fromUserText(texture)
            read_node['raw'].setValue(1)
            read_node['postage_stamp'].setValue(0)
            colorSpace = nuke.nodes.OCIOColorSpace()
            
            colorSpace['in_colorspace'].setValue('Utility - Linear - sRGB')
            if 'Color' in j:
                outC = 'ACES - ACEScg'
                colorSpace['out_colorspace'].setValue('ACES - ACEScg')
                newname = old.replace('.exr', '._acescg.exr')
            else:
                outC = 'Utility - Raw'
                colorSpace['out_colorspace'].setValue('Utility - Raw')
                newname = old.replace('.exr', '._raw.exr')

            colorSpace.setInput(0, read_node)

            erode = nuke.nodes.FilterErode()

            erode['channels'].setValue('rgb')
            erode['size'].setValue(-2)
            erode.setInput(0, colorSpace)
        
            mrg = nuke.nodes.Merge()
            mrg.setInput(1, colorSpace)
            mrg.setInput(0, erode)
            
            wrt = nuke.nodes.Write()
            wname = newname.replace('/wip/', '/out/')

            wrt['file'].fromUserText(wname)
            wrt['colorspace'].setValue(outC)
        
            wrt.setInput(0, mrg)
            wrt['cgUIR'].execute()

_autoplace()