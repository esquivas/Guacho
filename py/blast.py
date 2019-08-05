#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import struct
from guacho_utils import *
from matplotlib.colors import LogNorm

plt.ion()
#rmin=.5
#rmax=1.

path = '../picBlast/BIN/'
nout = 9

nproc = get_Nproc(nout,path=path)

rho  = get_2d_cut(3,1,nout=nout,neq=0,path=path,verbose=False)
vx   = get_2d_cut(3,1,nout=nout,neq=1,path=path,verbose=False)
vy   = get_2d_cut(3,1,nout=nout,neq=2,path=path,verbose=False)

shockF = get_2d_cut(3,1,nout=nout,neq=0,path=path,base='shock-',verbose=False)
plt.figure(2)
plt.clf()
#plt.imshow(shockF, extent=[0,1,0,1], origin='lower', cmap='viridis',interpolation = 'none' )
plt.imshow(shockF.T, extent=[0,1,0,1], cmap='viridis',interpolation = 'none' )
plt.colorbar()

#divV = readbin3d_all(nout=nout,neq=0,path=path,base='divV-',verbose=False)
#X,Y = np.meshgrid( np.linspace(-1.,1.,num=rho.shape[0]),np.linspace(-1.,1.,num=rho.shape[1]) )

dx = 1./128
extent =  [-0.5*dx,128.5*dx,0,1]
extent =  [0,1,0,1]

plt.figure(1)
plt.clf()
plt.imshow(rho, extent=extent, origin='lower', cmap='Spectral' )
plt.colorbar()

#plt.figure(2)
#plt.clf()
#plt.imshow(divV, oriin='lower', cmap='Spectral' )
#plt.colorbar()

#Q= plt.quiver(X[::4],Y[::4],vx[::4],vy[::4], pivot='mid',scale=20)
plt.figure(3) ; plt.clf()

npart = 250
for (noutp) in range(nout+1):
    picData, SED= readpic(noutp,path=path)
    print(picData.shape)
    plt.figure(1)
    plt.plot(picData[:,1],picData[:,2],'o',markersize= 1)
    plt.plot(picData[npart,1],picData[npart,2],'*',markersize=8, color='green')
    plt.figure(3)
    plt.loglog(SED[npart,:,0],SED[npart,:,1]*SED[npart,:,0]**2,label=str(noutp))
#    for ip in range(256):
#      plt.loglog(SED[ip,:,0],SED[ip,:,1])
plt.legend()

plt.figure(2)
plt.plot(picData[:,1],picData[:,2],'o',markersize=5, color="red",alpha=0.5)

#    plt.clf()

#for ip in range(4096):
#    plt.plot(part[:,ip,0],part[:,ip,1],'-o',markersize= 1)
#    plt.xlim([0,1])
#    plt.ylim([0,1])

picDataS = readpic(nout,path=path, base='pic-shocked-')
plt.figure(2)
plt.plot(picDataS[:,1], picDataS[:,2], '*', markersize=5, color='blue',alpha=0.5)