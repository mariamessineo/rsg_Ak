import numpy as np
import pandas as pd
import matplotlib.ticker as ticker
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.2125, 0.7154, 0.0721])


def lbxy(wx,wy,dist,rsun):
  from astropy import units as u
  from astropy.coordinates import SkyCoord
  c = SkyCoord(ra=wx*u.degree, dec=wy*u.degree, frame='icrs')
  c.galactic
  long=c.galactic.l.degree
  lat=c.galactic.b.degree
  pi=np.pi
  xr=dist*np.sin(long*pi/180)*np.cos(lat*pi/180)          
  yr=dist*np.cos(long*pi/180)*np.cos(lat*pi/180)-rsun   
  zr= dist*np.sin(lat*pi/180)
  return xr,yr
 


def bg_im():
  im = plt.imread('main_milkyway-full_nasa_jpl-caltech.jpg')
  lo=14.5
  sh=0.0

  fig = plt.figure(figsize=(10, 10))
  ax1 = fig.add_subplot(111) 
  scale_x = 0.01666 
  scale_y = 0.01666 
  gc_x=0
  gc_y=0
  No_x=im.shape[0]/2-94+60
  No_y=im.shape[1]/2+60-60 

  ll=lo+2
  starx1=int((-1*ll-0.0)/scale_x+No_x)
  stary1=int((-1*ll-sh-0.0)/scale_y+No_y)
  print(starx1,stary1)
  starx2=int((ll+sh-0.0)/scale_x+No_x)
  stary2=int((ll-0.0)/scale_y+No_y)
  print(starx2,stary2)
  No_x=No_x-starx1
  No_y=No_y-stary1
  im2=im[starx1:starx2,stary1:stary2,0:3]
  im=im2

  ll=lo+1
  starx1=int((-1*ll-0.0)/scale_x+No_x)
  stary1=int((-1*ll-sh-0.0)/scale_y+No_y)
  print(starx1,stary1)
  starx2=int((ll+sh-0.0)/scale_x+No_x)
  stary2=int((ll-0.0)/scale_y+No_y)
  print(starx2,stary2)
  No_x=No_x-starx1
  No_y=No_y-stary1
  im2=im[starx1:starx2,stary1:stary2,0:3]
  im=im2

  ll=lo
  starx1=int((-1*ll-0.0)/scale_x+No_x)
  stary1=int((-1*ll-sh-0.0)/scale_y+No_y)
  print(starx1,stary1)
  starx2=int((ll+sh-0.0)/scale_x+No_x)
  stary2=int((ll-0.0)/scale_y+No_y)
  print(starx2,stary2)
  No_x=No_x-starx1
  No_y=No_y-stary1
  im2=im[starx1:starx2,stary1:stary2,0:3]
  im=im2
  return im,scale_x,scale_y,No_x,No_y


def get_fig(im,scale_x,scale_y,No_x,No_y,rsun,xr,yr,outeps,labo):
  fig = plt.figure(figsize=(10, 10))
  rect_1 = [ 0.15, .15, 0.845, .845]
  ax1 = fig.add_subplot(rect_1) 
  gray = -1*rgb2gray(im) 
  implot = plt.imshow(gray,cmap='gray')
  mcx=(0.0-0.0)/scale_x+No_x
  mcy=(0.0-rsun)/scale_y+No_y
  plt.scatter(mcx , mcy , c="b", s=7)
  print(mcx,mcy)
  plt.scatter(No_x , No_y , c="b", s=5)
  print(No_x,No_y)

  plt.xlabel(r'X [kpc]')
  plt.ylabel(r'Y [kpc]')

  starx=(xr-0.0)/scale_x+No_x
  stary=(yr-0.0)/scale_y+No_y
  plt.scatter(starx , stary , c="r", s=2)

  xx=np.array([-15,-10,-5,0,+5,+10,+15])
  yy=xx
  posx=xx/scale_x+No_x
  posy=-1*yy/scale_y+No_y

  ax1.xaxis.set_major_locator(ticker.FixedLocator((posx)))
  ax1.xaxis.set_major_formatter(ticker.FixedFormatter((xx)))
  ax1.yaxis.set_major_locator(ticker.FixedLocator((posy)))
  ax1.yaxis.set_major_formatter(ticker.FixedFormatter((yy)))

  props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
  textstr = "Image Credit: NASA/JPL-Caltech/R. Hurt (SSC/Caltech)"
  ax1.text(0.02, 0.05, textstr, transform=ax1.transAxes, fontsize=9,
        verticalalignment='top')
 
  props = dict(boxstyle='round', facecolor='red', alpha=0.5)
  textstr = labo
  ax1.text(0.8, 0.9, textstr, transform=ax1.transAxes, fontsize=9,color='red',
        verticalalignment='top')

  plt.savefig(outeps)
  return

  
rsun=8.125
ingaia="myfile.csv"
data=pd.read_csv(ingaia)
wx=data['raicrs']
wy=data['decicrs']
dist=data['r_med_geo'].values/1000.

xr,yr=lbxy(wx,wy,dist,rsun)
im,scale_x,scale_y,No_x,No_y=bg_im()
get_fig(im,scale_x,scale_y,No_x,No_y,rsun,xr,yr,'MWrsg.eps')



