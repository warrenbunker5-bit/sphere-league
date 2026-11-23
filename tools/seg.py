import sys,json,numpy as np
from PIL import Image,ImageDraw
from scipy import ndimage
n=sys.argv[1];im=Image.open(n+'.png').convert('RGBA');a=np.array(im)
fg=a[...,3]>40
# drop text labels: small/thin components near bottom are filtered by area
lab,k=ndimage.label(ndimage.binary_closing(fg,iterations=2))
objs=ndimage.find_objects(lab);P=[]
for i,sl in enumerate(objs,1):
  ar=(lab[sl]==i).sum()
  if ar<600:continue
  ys,xs=sl;P.append(dict(i=i,x0=xs.start,y0=ys.start,x1=xs.stop,y1=ys.stop,area=int(ar)))
P.sort(key=lambda p:(round(p['y0']/60),p['x0']))
sheet=Image.new('RGBA',(1400,900),(40,40,60,255));d=ImageDraw.Draw(sheet);x=y=10;rowh=0
for j,p in enumerate(P):
  c=im.crop((p['x0'],p['y0'],p['x1'],p['y1']));m=(lab[p['y0']:p['y1'],p['x0']:p['x1']]==p['i']);ca=np.array(c);ca[...,3]=np.where(m,ca[...,3],0);c=Image.fromarray(ca)
  s=min(2.0,180/max(c.size));c=c.resize((int(c.width*s),int(c.height*s)))
  if x+c.width>1390:x=10;y+=rowh+30;rowh=0
  sheet.alpha_composite(c,(x,y+18));d.text((x,y),f"{j}:{p['x1']-p['x0']}x{p['y1']-p['y0']}",fill='yellow');x+=c.width+20;rowh=max(rowh,c.height+18)
sheet.save(n+'_pieces.png');json.dump(P,open(n+'_pieces.json','w'));print(n,len(P),[ (j,p['x0'],p['y0'],p['x1']-p['x0'],p['y1']-p['y0']) for j,p in enumerate(P)])
