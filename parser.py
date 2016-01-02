#!/usr/bin/python

# Open a file
import os

class Coord(object):
    
    def __init__(self, line,x, y, z):
        """Constructeur de notre classe"""
	self.line = line
        self.x = x
        self.y = y
        self.z = z

def removeE( strInput ):
	chars = set('?')
	if any((c in chars) for c in strInput):
   		strInput = 0
	strInput = '%.3f' % round(float(strInput), 3)
	return strInput;

coord_list = []


fo = open("E9_VOITURE.stp", "rw+")

print "Name of the file: ", fo.name
newLayerPos = 0
fileNumber = 0

if not os.path.exists("Eclipse_gcode"):
	os.mkdir("Eclipse_gcode")


while True:
    try:
        line = fo.readline().strip()
	line = fo.readline()
	line = line.translate(None, '#=CARTESIAN_POINT Control Point Limit Line Origine();\'Lege')
	pline, pz, py, px = line.split(",")
	pline = removeE(pline)
	px= removeE(px)
	py = removeE(py)
	pz = removeE(pz)
	pline = float(pline)
	px = float(px)
	py = float(py)
	pz = float(pz)
	pzBuffer = float(pz)
	fo.seek(newLayerPos)# set cursor to 0

	while (pz == pzBuffer):
		coord_list.append(Coord(pline,px,py,pz))
		print "Coord: %u,%f,%f,%f" % (pline,px,py,pz)
		coord = Coord(0,0,0,0)	
		line = fo.readline()
		line = line.translate(None, '#=CARTESIAN_POINT Control Point Limit Line Origine();\'Lege')
		pline, pz, py, px = line.split(",")
		pline = removeE(pline)
		px= removeE(px)
		py = removeE(py)
		pz = removeE(pz)
		pline = float(pline)
		px = float(px)
		py = float(py)
		pz = float(pz)

	# create the new file
	filename = "Eclipse_gcode/layer_%d.ngc" % (fileNumber)
	fileNumber = fileNumber+1
	file = open(filename, 'w+')
	for coord in coord_list:
		gcodeLine = "G01 X%f Y%f\n\r" % (coord.x,coord.y)
		file.write(gcodeLine)
	del coord_list[:]
	newLayerPos = fo.tell()
	print "newfile"
    except EOFError:
        break #

#line = fo.readline()
#print "Read Line: %s" % (line)
# Get the current position of the file.


# Close opend file
fo.close()
