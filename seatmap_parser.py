from xml.etree import ElementTree as ET
import json
import sys 
import os

filename = sys.argv[1]

tree = ET.parse(filename)
root = tree.getroot()


# --- FUNCTIONS -------------------------------------------------------------------

# --- OT functions --------------

def OT_get_price ( seatElement ):
    
    serviceFee = seatElement.find('ns:Service/ns:Fee', namespaces)
    
    if serviceFee is None:
        return 'NA'
    else:
        
        price = int( serviceFee.attrib['Amount'] ) / (10 ** int( serviceFee.attrib['DecimalPlaces']) )
        return price
    
def OT_get_availability ( seatElement ):
    
    availability = seat.find('ns:Summary', namespaces ).attrib['AvailableInd']
    
    if availability == 'true':
        return True
    elif availability == 'false':
        return False
    else:
        return 'NA'
    
    
def OT_get_type ( seatElement ):
    
    features = seatElement.findall('ns:Features', namespaces)
    
    for feature in features:
        
        if 'extension' in feature.attrib:
       
            extension = feature.attrib['extension']
        
            if extension == "Lavatory":
                return 'lavatory'
        
    return 'seat'    

# --- IATA functions ------------

def IATA_get_price ( seatElement ):
    
    service = seatElement.find('ns:OfferItemRefs', namespaces)
    
    if service is None:
        return 'NA'
    
    serviceCode = service.text 
    
    if serviceCode in prices.keys():
        return float(prices[serviceCode])
    else:
        return 'NA'
    
def IATA_check_code ( seatElement, code ):
    
    seatCodes = [ el.text for el in seatElement.findall('ns:SeatDefinitionRef', namespaces) ]
    
    if code in seatCodes:
        return True
    else:
        return False
    
# --- MAIN ------------------------------------------------------------------------


seatmap = []

# check tipe of file: OPEN TRAVEL
if root.tag == '{http://schemas.xmlsoap.org/soap/envelope/}Envelope':
    
    namespaces = {'ns'      : 'http://www.opentravel.org/OTA/2003/05/common/',
                  'soapenv' : 'http://schemas.xmlsoap.org/soap/envelope/'}


    # get seatmaps
    clases = root.findall('soapenv:Body/ns:OTA_AirSeatMapRS/ns:SeatMapResponses/ns:SeatMapResponse/ns:SeatMapDetails/ns:CabinClass', namespaces)
    
    for clase in clases:
        for row in clase.findall( 'ns:RowInfo', namespaces ):
            for seat in row.findall( 'ns:SeatInfo', namespaces ): 
                            
                seatinfo = { 
                    'Element_type' : OT_get_type( seat ),
                    'Seat_id'      : seat.find('ns:Summary', namespaces ).attrib['SeatNumber'],
                    'Seat_price'   : OT_get_price( seat ),
                    'Cabin_class'  : row.attrib['CabinType'],
                    'Availability' : OT_get_availability( seat )
                    }
                
                seatmap.append( seatinfo )

# check tipe of file: IATA
if root.tag == '{http://www.iata.org/IATA/EDIST/2017.2}SeatAvailabilityRS':

    namespaces = {'ns' : 'http://www.iata.org/IATA/EDIST/2017.2'}

    # get prices codes
    prices = {}
    
    for element in root.findall('ns:ALaCarteOffer/ns:ALaCarteOfferItem', namespaces):
        prices[element.get('OfferItemID')] = element.find('ns:UnitPriceDetail/ns:TotalAmount/ns:SimpleCurrencyPrice', namespaces).text

    # get seatmaps
    for seatmapelement in root.findall('ns:SeatMap', namespaces):
        for row in seatmapelement.findall('ns:Cabin/ns:Row', namespaces):
            
            rowNumber = row.find('ns:Number',namespaces).text
            
            for seat in row.findall('ns:Seat', namespaces):
                
                column = seat.find('ns:Column', namespaces).text
                
                seatinfo = { 
                    'Element_type' : 'seat',
                    'Seat_id'      : rowNumber + column,
                    'Seat_price'   : IATA_get_price( seat ),
                    'Cabin_class'  : 'Economy' if int(rowNumber) > 6 else 'First',
                    'Availability' : IATA_check_code( seat , 'SD4' )
                    }
                
                seatmap.append( seatinfo )

# write json file
filename = os.path.splitext(filename)[0]

with open('./' + filename + '_parsed.json', 'w') as outputFile :
    json.dump( seatmap , outputFile)
    

