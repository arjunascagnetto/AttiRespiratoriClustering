import matplotlib.pyplot as plt
import numpy as np
import os, sys, easygui
from collections import deque
from matplotlib.font_manager import FontProperties
from matplotlib import gridspec

# zero for testing only
plotVar = 1

def nta_file_parser(file_data):
    dat.clear()
    f = open(file_data[2],'r')
    lines = f.readlines()
    for line in lines:
        if not line.startswith('%'):
            dat.append(line.replace('\n','').split('\t',8))
    v = np.ndarray(shape=(len(dat),4),dtype=float)
    for i in range(len(dat)):
        for j in range(3,7): # prende solo le colonne 4 5 6 7 
            v[i-3,j-3]=float(dat[i][j])
    return v

def ndata(data2norm):
    #data2norm = data2norm/np.max(np.abs(data2norm))
    data2norm = data2norm
    return data2norm

def gen_subplot(Num_of_images,data,file_data):
    for i in range(0,Num_of_images):
        fontP = FontProperties()
        fontP.set_size('8')
        fig = plt.figure(figsize=(20, 10)) 
        cycle = np.asarray(data[i])
        start = cycle[0,0]
        end = cycle[-1,0]
        t = np.arange(start,end+1,1)
        
        # Preparo la griglia
        gs = gridspec.GridSpec(3, 3)

        axC = plt.subplot(gs[0:3, 0:2])
        axF = plt.subplot(gs[0, 2])
        axP = plt.subplot(gs[1, 2])
        axEA = plt.subplot(gs[2, 2])

        # Plot dei CICLI
        axC.set_color_cycle(['black', 'red'])
        axC.plot(cycle[:,1],cycle[:,2],cycle[:,1],np.zeros(len(cycle[:,1])))
        axC.set_title(('from',str(start),'to',str(end)))
        axC.set_xlabel('Pressione')
        axC.set_ylabel('Flusso')
                
        # Plot delle serie temporali
        axP.set_xlim(start,end)
        axP.plot(t,ndata(cycle[:,1]),'r',label='Pressione')
        axP.legend(loc='upper right',prop = fontP)
        axF.set_xlim(start,end)
        axF.plot(t,ndata(cycle[:,2]),'b',label='Flusso')
        axF.legend(loc='upper right',prop = fontP)
        axEA.set_xlim(start,end)
        axEA.plot(t,ndata(cycle[:,3]),'g',label='EAdi')
        axEA.legend(loc='upper right',prop = fontP)
        
        # Output a file png
        image_filename = "".join((file_data[3],file_data[1],'-',str(i+1),'.png'))
        if plotVar:
            print "Saving",image_filename
            plt.savefig(image_filename)
        plt.close()

def build_data(v):
    length = len(v)
    st = v[:,0] # States 0 inspirio 1 espirio
    pr = v[:,1] # Pressure
    fl = v[:,2] # Flow
    ed = v[:,3] # EADI
    c = 1
    d.clear()
    print '\n\t',len(d),'\n'
    l = []
    #np.split(x, np.nonzero(np.diff(x) == 1)[0]+1)
    for i in range(length):
        if st[i] == 1:
            if c == 0:
                d.append(l)
                l = []
                c = 1
            l.append([i+1,pr[i],fl[i],ed[i]])
        else:
            if c == 1:
                c = 0
            l.append([i+1,pr[i],fl[i],ed[i]])
    # append of the last cycle
    d.append(l)
    return d

# MAIN LOOP
sdir = easygui.diropenbox()
dat = deque()
d = deque()
for subdir, dirs, files in os.walk(sdir):
    filenames = os.listdir(subdir)
    for filename in filenames:
        if 'ServoCurveData' in filename:
            images_subdir = "".join((subdir,'/images/'))
            file_path = "".join((subdir,'/',filename))
            #print images_subdir
            if not os.path.exists(images_subdir):
                os.makedirs(images_subdir)
            file_data = [subdir,filename,file_path,images_subdir]
            #print 'SUBDIR',subdir,'FILENAME',filename
            vector = nta_file_parser(file_data)
            deque = build_data(vector)
            nIm = len(deque) # Number of Images
            gen_subplot(nIm,deque,file_data)