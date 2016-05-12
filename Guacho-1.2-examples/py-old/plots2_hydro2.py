from guachoUtils import *
import matplotlib as mpl
from mpl_toolkits.axes_grid1 import ImageGrid
from matplotlib.colors import LogNorm
from matplotlib import rc
import matplotlib.pyplot as plt

rc('text', usetex=True)

mpl.rc('xtick',labelsize=10)
mpl.rc('ytick',labelsize=10)
mpl.rc('text',usetex=True)
#mpl.rc('font',**{'family':'serif','serif':['Computer Modern']})

def add_inner_title(ax, title, loc, size=None, **kwargs):
    from matplotlib.offsetbox import AnchoredText
    from matplotlib.patheffects import withStroke
    if size is None:
        size = dict(size=plt.rcParams['ytick.labelsize'])
    at = AnchoredText(title, loc=loc, prop=size,
                      pad=0., borderpad=0.5,
                      frameon=False, **kwargs)
    ax.add_artist(at)
    at.txt._text.set_path_effects([withStroke(foreground="w", linewidth=4)])
    return at


nxtot=100 #256
nytot=25  #64
nztot=100 #256
mpiX=2 #4
mpiY=1
mpiZ=2 #4
neqs=10


cv=100.
gam=(cv+1.)/cv
vsc=np.sqrt(gam*8.31e7*1e4/1.3)/1e5
tempsc=1e4*gam
psc=1.66e-24*vsc*vsc

firstrun=True
plt.ion()

run='P2'

path='../P2/BIN/'


for nout in range(0,30):
    #  this is the ionization rate
    if (firstrun):
#        Phi = coplot3d(2,nytot/2,0,1,nxtot,nytot,nztot,mpiX,mpiY,mpiZ,nout,nghost=0,path=path,base='ph-')
#        temp= coplotTemp(2,nytot/2,neqs,nxtot,nytot,nztot,mpiX,mpiY,mpiZ,nout,path=path,cv=cv,Tempsc=tempsc)
        denT= coplot3d(2,nytot/2,0,neqs,nxtot,nytot,nztot,mpiX,mpiY,mpiZ,nout,path=path)
        vx=   coplot3d(2,nytot/2,1,neqs,nxtot,nytot,nztot,mpiX,mpiY,mpiZ,nout,path=path)/denT*vsc
        vz=   coplot3d(2,nytot/2,3,neqs,nxtot,nytot,nztot,mpiX,mpiY,mpiZ,nout,path=path)/denT*vsc
        Pgas= coplot3d(2,nytot/2,4,neqs,nxtot,nytot,nztot,mpiX,mpiY,mpiZ,nout,path=path)*psc
        denN= coplot3d(2,nytot/2,5,neqs,nxtot,nytot,nztot,mpiX,mpiY,mpiZ,nout,path=path)
    
        magv=np.sqrt(vx*vx+vz*vz)
        Pram= denT*magv*magv
#        yhp=1.-denN/denT
#        Phi=Phi+1e-30
#        Psi= Phi*denN+1e-30    
    #map3d=readbin3d(0,neqs,nxtot,nytot,nztot,mpiX,mpiY,mpiZ,nout,path='/datos_diable/esquivel/ExoGuacho/GR/')
    
#    images=[denT,denN,temp,Pgas,Phi,Psi,yhp,magv,Pram]
        images=[denT,denN,Pgas,Pram,magv]

#    cmaps=['Blues_r','Blues','gist_heat','jet','gist_heat','jet' ,'seismic','jet','Spectral']
        cmaps=['Blues_r','Blues','gist_heat','jet','Spectral']
    
#    minVs=[100.,  100, 1e4, 1E-15, 1e-8, 1e-4 , 0,    0 , 1e4 ]
#    maxVs=[1e10, 1e10, 1e5, 1e-11, 1e-4, 1e1  , 1., 600 , 1e11]
        minVs=[100.  ,  100  , 1E-22, 1e2 , 1     ]
        maxVs=[0.5e10, 0.5e11, 1e-16, 1e11, 700    ]

# SIZE OF FIGURE
    F = plt.figure(1, (10, 10))
    F.clf()
    grid = ImageGrid(F, 111,nrows_ncols = (2, 3),direction="row",axes_pad = 0.2, add_all=True,
                 label_mode = "1", share_all = False, cbar_location="top", cbar_mode="each",
                 cbar_size="5.%",cbar_pad="1.%" )

    extent=(-0.175,0.175,-0.175,0.175)
        
#    for i in range(0,9):
    for i in range(0,5):
        
        if (i >= 4) :
            norms=None
        else:
            norms=LogNorm()
        
        im=grid[i].imshow(images[i],cmap=cmaps[i],origin='lower'
                      ,extent=extent, vmin=minVs[i],vmax=maxVs[i] , norm=norms )

        #lvls = np.logspace(np.log10(minVs[i]),np.log10(maxVs[1]),3)
        
        grid[i].cax.colorbar(im, extend='none')
        grid[i].cax.toggle_label(True)

        
#   for ax, im_title in zip(grid, [r"(a) XZ $n_{tot}$", r"(b) XZ $n_{H0}$",r"(c) XZ $T$",
#                                  r"(d) XZ $P_{th}$",  r"(e) XZ $\phi$",  r"(f) XZ $\Psi/(kT)$" ,
#                                  r"(g) XZ $y_{H^+}$", r"(h) XZ $|v|$",r"(i) XZ $\rho v^2$"]):
    for ax, im_title in zip(grid, [r"(a) XZ $n_{tot}$", r"(b) XZ $n_{H0}$",r"(c) XZ $P_{th}$",
                                   r"(d) XZ $\rho v^2$",  r"(e) XZ $|v|$",  r"(f) XZ $\Psi/(kT)$"]):

        t = add_inner_title(ax, im_title,loc=2 )
        t.patch.set_ec("none")
        t.patch.set_alpha(1.0)
            
    #grid[0].cax.text(550.,9.5,r'Density [cm$^{-3}$]')
    grid[0].cax.text(1000.,8.,r't='+str(nout*0.05).format('f')+' days')

    plt.savefig(run+'-'+str(nout).zfill(3)+'.png',dpi=300,transparent=True,bbox_inches='tight')
    #plt.savefig('./fig.eps',dpi=300,transparent=True,bbox_inches='tight',facecolor='gray')
    
    fig = plt.gcf()
    fig.set_size_inches(6.,6.)
    
    plt.draw()
    plt.show()
    
#plt.ioff()


