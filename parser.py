
# Open a file
import os
import sys
import math
from operator import attrgetter

class Coord(object):
    
    def __init__(self, line,x, y, z, a, pyth):
        """Constructeur de notre classe"""
        self.line = line
        self.x = x
        self.y = y
        self.z = z
	self.a = a
        self.pyth = pyth

def removeE( strInput ):
    chars = set('?')
    if any((c in chars) for c in strInput):
        strInput = 0
    strInput = '%.2f' % round(float(strInput), 2)
    return strInput;

rawCoord_list = []
pyth_list = []
orgCoord_list = []

#ouverture du fichier a decouper
fo = open("E9_VOITURE_V2.stp", "r")

print "Name of the file: ", fo.name
newLayerPos = 0
fileNumber = 0

#creation du dossier des fichiers
if not os.path.exists("Eclipse_gcode"):
    os.mkdir("Eclipse_gcode")

#pour toute les ligne du fichier source
while True:
    try:
        line = fo.readline().strip()
        fo.seek(newLayerPos)# set cursor to new position
        #read layer first line
        line = fo.readline()
        line = line.translate(None, '#=CARTESIAN_POINT\ ControlPointLimitLineOrigine();\'Lege')# remove character in the string
        pline, px, py, pz = line.split(",")# split string in float string
        #remove E-**
        pline = removeE(pline)
        px= removeE(px)
        py = removeE(py)
        pz = removeE(pz)
        #cast string in float
        pline = float(pline)
        px = float(px)
        py = float(py)
        pz = float(pz)
        # save z buffer
        pzBuffer = float(pz)

        #while there is no new z layer
        while (pz == pzBuffer):
            rawCoord_list.append(Coord(pline,px,py,pz,0,math.hypot(px,py)))
    #       print "Coord: %u,%.3f,%.3f,%.3f,%.3f" % (pline,px,py,pz,pzBuffer)
            coord = Coord(0,0,0,0,0,0)    
            line = fo.readline()
            line = line.translate(None, '#=CARTESIAN_POINT Control Point Limit Line Origine();\'Lege')# remove character in the string
            pline, px, py, pz = line.split(",")# split string in float string
            #remove E-**
            pline = removeE(pline)
            px= removeE(px)
            py = removeE(py)
            pz = removeE(pz)
            #cast string in float
            pline = float(pline)
            px = float(px)
            py = float(py)
            pz = float(pz)

        #organize Data--------------------------
        firstValue = min(rawCoord_list,key=attrgetter('pyth'))#find the first value
        #delete this value from the raw list
        lindex = rawCoord_list.index(firstValue)
        del rawCoord_list[lindex]
        actualPoint = firstValue# set the actual point  
        orgCoord_list.append(actualPoint)# add this point to the organized list
        # while not every value have been prosessed
        while len(rawCoord_list) > 0 :
            # compute hypotenuse for every remaining point
            for coord in rawCoord_list:
                coord.pyth = math.hypot(coord.x-actualPoint.x,coord.y-actualPoint.y)
            actualPoint = min(rawCoord_list,key=attrgetter('pyth'))# set the next point to the smallest hypotenuse
            orgCoord_list.append(actualPoint)#add this point to the orginized list  
            # delete this point from the raw list   
            lindex = rawCoord_list.index(actualPoint)
            del rawCoord_list[lindex]

        for index, coord in enumerate(orgCoord_list):
            try:
                orgCoord_list[index].a=(orgCoord_list[index].y-orgCoord_list[index-1].y)/(orgCoord_list[index].x-orgCoord_list[index-1].x)
            except ZeroDivisionError:
                del orgCoord_list[index]

            try:
                ca = orgCoord_list[index-1].a
            except IndexError:
                ca = max(rawCoord_list,key=attrgetter('pyth'))
            try:    
                if (orgCoord_list[index].a == ca):
                    del orgCoord_list[index-1]
            except IndexError:
                caca=0

        orgCoord_list.append(orgCoord_list[0])# close the loop with the first point

        for coord in orgCoord_list:
            coord.x = coord.x/25.4
            coord.y = coord.y/25.4
        
        

        
        # create the new file
        filename = "Eclipse_gcode/layer_%d.tap" % (fileNumber)
        print "layer_%d number of point: %d" % (fileNumber,len(orgCoord_list))
        fileNumber = fileNumber+1
        file = open(filename, 'w+')
        gcodeLine = "; number of position %d\n\r" % (len(orgCoord_list))
        file.write(gcodeLine)
        #write the organized cordinate in the new file
        for coord in orgCoord_list:
            gcodeLine = "G01 X%.3f Y%.3f Z%.3f A%.3f\n\r" % (coord.x,coord.y,coord.x,coord.y)
            file.write(gcodeLine)
        del orgCoord_list[:]#clear the list for the next document
        newLayerPos = fo.tell() 
    #   print "layer_%d" % (fileNumber)
    except EOFError:
        break #


# Close opend file
fo.close()
