#This code presents the CT scans selection algortihm from https://github.com/mr7495/COVID-CT-Code
import os
import numpy as np
import cv2
import shutil


def find_inds(ch,st): #function to find the indexes of a character in a string
    indexes=[]
    index0=0
    num=0
    while(True):
        if ch in st[num:]:
            index0=st[num:].index(ch)
            indexes.append(index0+num)
            num=num+index0+1
        else:
            break
    return(indexes)


!mkdir('selected_TIF')#path to save the selected TIFF images

original_path='COVID-CTset' #Path to the original dataset
adds={}
for r,d,f in os.walk(original_path): #Take the addresses of the TIFF files for each patient in the dataset
    for file in f:
        if'.tif' in file:
            full_add=os.path.join(r,file)
            indexes=find_inds('\\',full_add)
            index=indexes[-1]
            if full_add[:index+1] not in adds:
                adds[full_add[:index+1]]=[]
            adds[full_add[:index+1]].append(full_add[index+1:])

selected={}            
for key in adds:
    zero=[]
    names=[]
    for value in adds[key]:
        names.append(value)
        address=key+value
        pixel=cv2.imread(address,cv2.IMREAD_UNCHANGED ) #read the TIFF file
        sp=pixel[240:340,120:370] #Crop the region
        counted_zero=0
        for i in np.reshape(sp,(sp.shape[0]*sp.shape[1],1)):
            if i<300: #count the number of pixel values in the region less than 300
                counted_zero+=1
        zero.append(counted_zero)
    min_zero=min(zero)
    max_zero=max(zero)
    threshold=(max_zero-min_zero)/1.5 #Set the threshold
    indices=np.where(np.array(zero)>threshold) #Find the images that have more dark pixels in the region than the calculated threshold
    selected_names=np.array(names)[indices]
    selected[key]=list(selected_names) #Add the selected images of each patient
    

#Copy the selected images to the new folder
for key in selected:
    indexes=find_inds('\\',key)
    for i in range(4):
        globals()['index{}'.format(i+1)]=indexes[i]
    try:
        os.mkdir('selected_TIF/{}'.format(key[index1+1:index2]))
    except:
        pass
    try:
        os.mkdir('selected_TIF/{}/{}'.format(key[index1+1:index2],key[index2+1:index3]))
    except:
        pass 
    try:
        os.mkdir('selected_TIF/{}/{}/{}'.format(key[index1+1:index2],key[index2+1:index3],key[index3+1:index4]))
    except:
        pass 
    for value in selected[key]:
        address=key+value
        new_address='selected_TIF'+address[3:]
        shutil.copy(address,new_address)

        

