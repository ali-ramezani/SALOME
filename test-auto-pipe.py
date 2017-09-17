# -*- coding: utf-8 -*-

###
### This file is generated automatically by SALOME v7.8.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
theStudy = salome.myStudy

import salome_notebook
notebook = salome_notebook.NoteBook(theStudy)
sys.path.insert( 0, r'/home/ali/salome')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New(theStudy)

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

def vm(a,b):
    return [a[0]-b[0],a[1]-b[1],a[2]-b[2]]

def vp(a,b):
    return [a[0]+b[0],a[1]+b[1],a[2]+b[2]]

def vpp(a,b,c):
    return [a[0]+b[0]*c,a[1]+b[1]*c,a[2]+b[2]*c]
    

def vdot(a,b):
    return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]

def vlen(a,b):
    t=vm(b,a)
    l2=vdot(t,t)
    return math.sqrt(l2)

def vnor(a):
    b=[0,0,0]
    ll=vlen(a,b)
    return [a[0]/ll,a[1]/ll,a[2]/ll]

def vcross(a,b):
    return [(a[1]*b[2]-a[2]*b[1]),(a[2]*b[0]-a[0]*b[2]),(a[0]*b[1]-a[1]*b[0])]
    
def Cyl(iv1,iv2,rad):
    norc=vm(iv2,iv1)
    v1 = geompy.MakeVertex(iv1[0], iv1[1], iv1[2])
    nor = geompy.MakeVectorDXDYDZ(norc[0], norc[1], norc[2])
    cyl = geompy.MakeCylinder(v1,nor,rad,vlen(iv1,iv2))
    return cyl
    
    
def CylBend(iv1,iv2,iv3,ir,irr):
    v1 = geompy.MakeVertex(iv1[0], iv1[1], iv1[2])

    ll=vlen(iv2,iv1)
    nor1=vm(iv2,iv1)
    nor1=vnor(nor1)


    ll2=vlen(iv3,iv2)
    nor2=vm(iv3,iv2)
    nor2=vnor(nor2)
    
    print nor1,nor2

    dd=vdot(nor1,nor2)
    an=math.acos(dd)
    print 'an=',an*180.0/math.pi
    
    v21c=vpp(iv2,nor1,-math.tan(an/2)*irr)
    v21 = geompy.MakeVertex(v21c[0],v21c[1],v21c[2])
    vnor1=geompy.MakeVectorDXDYDZ(nor1[0],nor1[1],nor1[2])
    print ir,vlen(iv1,v21c)
    cyl = geompy.MakeCylinder(v1,vnor1,ir,vlen(iv1,v21c))
    
    cir = geompy.MakeDiskPntVecR(v21, vnor1, ir)

    nor3=vcross(nor1,nor2)
    nor3=vnor(nor3)

    nor1o=vcross(nor3,nor1)
    nor1o=vnor(nor1o)

    v2cen=vpp(v21c,nor1o,irr)
    v2cen2=vp(v2cen,nor3)
    v23 = geompy.MakeVertex(v2cen[0],v2cen[1],v2cen[2])
    v24 = geompy.MakeVertex(v2cen2[0],v2cen2[1],v2cen2[2])
    v23v24 = geompy.MakeLineTwoPnt(v23, v24)

    bend = geompy.MakeRevolution(cir, v23v24,an)
    print nor1,nor2,nor3,v2cen,v2cen2
    Fuse_1 = geompy.MakeFuseList([cyl, bend], True, True)
    a=irr*math.sin(an)
    b=-irr*math.cos(an)
    v22c = [v2cen[0]+nor1[0]*a+nor1o[0]*b,v2cen[1]+nor1[1]*a+nor1o[1]*b,v2cen[2]+nor1[2]*a+nor1o[2]*b]
    return Fuse_1,v22c    

def AutoFiletCyl(path,filets,rad):
	nv=path[0]
	objs=[]
	for i in xrange(1,len(path)):
		v2=path[i]

		if (i+1)==len(path):
			obj=Cyl(nv,v2,rad)
		else:
			v3=path[i+1]
			obj,nv=CylBend(nv,v2,v3,rad,filets[i-1])

		objs.append(obj)
	return geompy.MakeFuseList(objs, True, True)
	
	
O,OX,OY,OZ=1,2,3,4

geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )

obj,nv=CylBend([0,0,0],[0,2,5],[4,0,6],0.2,1.5)
obj2=Cyl(nv,[4,0,6],0.2)
obj3=AutoFiletCyl([[0,0,0],[0,2,5],[4,0,6],[4,0,8],[6,9,2]],[1.5,1,0.5],0.1)

geompy.addToStudy( obj, 'obj' )
geompy.addToStudy( obj2, 'obj2' )
geompy.addToStudy( obj3, 'obj3' )


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser(1)
