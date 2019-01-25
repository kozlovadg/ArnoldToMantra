from shutil import copyfile
import os

def saveAndRename():
    # parsing folders with textures and rename it        
    parentFolder = folder_to_save_base
    names = []

    for i in os.listdir(parentFolder):
        for j in os.listdir(os.path.join(parentFolder, i)):
            if j.endswith("exr"):
                old = os.path.join(os.path.join(parentFolder, i), j)
                try:
                    new = os.path.join(os.path.join(parentFolder, i), i+j.split("Shape")[1])
                    names.append((old, new))
                except:
                    try:
                        new = os.path.join(os.path.join(parentFolder, i), i+j.split("outputCloth2")[1])
                        names.append((old, new))
                    except:
                        pass

    for i in range(len(names)):
        os.rename(names[i][0],names[i][1]) 

def copy():
    # parsing folders with textures and rename it        
    parentFolder = folder_to_save_base
    names = []

    for i in os.listdir(parentFolder):
        for j in os.listdir(os.path.join(parentFolder, i)):
            if j.endswith("txt"):
                fromCopy = os.path.join(os.path.join(parentFolder, i), j)
                toCopy = os.path.join(os.path.join(parentFolder, i), i + '.txt')
                try:
                    copyfile(fromCopy, toCopy)
                except:
                    pass
                break
folder_to_save_base = "/cg/projects/virtus/assets/robots/scenes/mark2/texturing/wip/v04/"

                  
saveAndRename()        
copy()