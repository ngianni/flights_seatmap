from xml.etree import ElementTree as ET
import json
import sys 

#print(sys.argv)

#xml_in= "seatmap1.xml"        

   


tree= ET.parse("seatmap1.xml")
root1 = tree.getroot()

tree= ET.parse("seatmap2.xml")
root2 = tree.getroot()



ns = "http://www.opentravel.org/OTA/2003/05/common/"

ns2= "http://www.iata.org/IATA/EDIST/2017.2"

data=[]


# 2- Seat price

for child in root1.iter("{" + ns + "}" + "Fee"):
    #print(child.tag)

    print(child.get("Amount"))



