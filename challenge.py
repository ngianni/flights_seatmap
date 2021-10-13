
'''

- Seat/Element type (Seat, Kitchen, Bathroom, etc)
	1- Seat id (17A, 18A)
	2- Seat price
	3- Cabin class
	4- Availability

'''


from xml.etree import ElementTree as ET
import json
import sys 
   
xml_in= sys.argv[1]   


tree= ET.parse(xml_in)
root1 = tree.getroot()

tree= ET.parse("seatmap2.xml")
root2 = tree.getroot()



ns = "http://www.opentravel.org/OTA/2003/05/common/"

ns2= "http://www.iata.org/IATA/EDIST/2017.2"

data=[]



#1- Seat number (17A, 18A) y 3- Cabin class

for i, child in enumerate (root1.iter("{" + ns + "}" + "RowInfo")):

     for seat in child.iter("{" + ns + "}" + "Summary"):

         for price in child.iter("{" + ns + "}" + "Fee"):

          data.append({"SeatNumber": seat.get("SeatNumber"),"CabinType": child.get("CabinType"), "Price": child.get("Amount")})
           

#4- Availability

for j, child in enumerate (root1.iter("{" + ns + "}" + "Summary")):
    
    data[j]["Available"] = child.get("AvailableInd")


# 2- Seat price

for p, child in enumerate (root1.iter("{" + ns + "}" + "Fee")):
    
   
   data[p]["Price"] = child.get("Amount")

#----------------------------------


data_json=json.dumps(data)

print(data_json)


















	









 


   


