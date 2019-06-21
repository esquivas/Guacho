#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
import struct
from guacho_utils import *
from matplotlib.colors import LogNorm

plt.ion()
rmin=.5
rmax=1.

path = '../pic/BIN/'
nout = 0

rho = get_2d_cut(3,1,nout=nout,neq=0,path=path,verbose=False)
vx  = get_2d_cut(3,1,nout=nout,neq=1,path=path,verbose=False)
vy  = get_2d_cut(3,1,nout=nout,neq=2,path=path,verbose=False)

X,Y = np.meshgrid( np.linspace(-5.,5.,num=rho.shape[0]),np.linspace(-5.,5.,num=rho.shape[1]) )

plt.figure(2)
plt.clf()
plt.imshow(rho, extent=[-5,5,-5,5], origin='lower', cmap='Spectral', vmin=rmin, vmax=rmax )
plt.colorbar()

Q= plt.quiver(X[::4],Y[::4],vx[::4],vy[::4], pivot='mid',scale=20)


part = np.zeros(shape=(50,512,2) )
for (nout) in range(50):
    npart, xp, yp, zp, vxp, vyp, vzp = readpic(nout,2,path=path)
    part[nout,:,0] = xp[:]
    part[nout,:,1] = yp[:]

for ip in range(npart):
    plt.plot(part[:,ip,0]-5,part[:,ip,1]-5,'o',markersize= 2)
    plt.xlim([-5,5])
    plt.ylim([-5,5])
