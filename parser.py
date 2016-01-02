#!/usr/bin/python

# Open a file
import os
import math
from operator import attrgetter

class Coord(object):
    
    def __init__(self, line,x, y, z, pyth):
        """Constructeur de notre classe"""
	self.line = line
        self.x = x
        self.y = y
        self.z = z
	self.pyth = pyth

def removeE( strInput ):
	chars = set('?')
	if any((c in chars) for c in strInput):
   		strInput = 0
	strInput = '%.3f' % round(float(strInput), 3)
	return strInput;

rawCoord_list = []
pyth_list = []
orgCoord_list = []


fo = open("E9_VOITURE_V2.stp", "rw+")

print "Name of the file: ", fo.name
newLayerPos = 0
fileNumber = 0

if not os.path.exists("Eclipse_gcode"):
	os.mkdir("Eclipse_gcode")


while True:
    try:
	fo.seek(newLayerPos)# set cursor to 0
        line = fo.readline().strip()
	line = fo.readline()
	line = line.translate(None, '#=CARTESIAN_POINT Control Point Limit Line Origine();\'Lege')
	pline, px, py, pz = line.split(",")
	pline = removeE(pline)
	px= removeE(px)
	py = removeE(py)
	pz = removeE(pz)
	pline = float(pline)
	px = float(px)
	py = float(py)
	pz = float(pz)
	pzBuffer = float(pz)


	while (pz == pzBuffer):
		rawCoord_list.append(Coord(pline,px,py,pz,math.hypot(px,py)))
		print "Coord: %u,%.3f,%.3f,%.3f,%.3f" % (pline,px,py,pz,pzBuffer)
		coord = Coord(0,0,0,0,0)	
		line = fo.readline()
		line = line.translate(None, '#=CARTESIAN_POINT Control Point Limit Line Origine();\'Lege')
		pline, px, py, pz = line.split(",")
		pline = removeE(pline)
		px= removeE(px)
		py = removeE(py)
		pz = removeE(pz)
		pline = float(pline)
		px = float(px)
		py = float(py)
		pz = float(pz)

	#organize Data--------------------------
	#find the first value
	firstValue = min(rawCoord_list,key=attrgetter('pyth'))
	lindex = rawCoord_list.index(firstValue)
	del rawCoord_list[lindex]	
	actualPoint = firstValue
	orgCoord_list.append(actualPoint)
	while len(rawCoord_list) > 0 :
		for coord in rawCoord_list:
			coord.pyth = math.hypot(coord.x-actualPoint.x,coord.y-actualPoint.y)
		actualPoint = min(rawCoord_list,key=attrgetter('pyth'))
		orgCoord_list.append(actualPoint)		
		lindex = rawCoord_list.index(actualPoint)
		del rawCoord_list[lindex]
	orgCoord_list.append(orgCoord_list[0])
	
	

	
	# create the new file
	filename = "Eclipse_gcode/layer_%d.tap" % (fileNumber)
	fileNumber = fileNumber+1
	file = open(filename, 'w+')
	for coord in orgCoord_list:
		gcodeLine = "G01 X%.3f Y%.3f A%.3f Z%.3f\n\r" % (coord.x,coord.y,coord.x,coord.y)
		file.write(gcodeLine)
	del orgCoord_list[:]
	newLayerPos = fo.tell()
	print "newfile"
    except EOFError:
        break #

#line = fo.readline()
#print "Read Line: %s" % (line)
# Get the current position of the file.


# Close opend file
fo.close()
