import snap, csv

from haversine import haversine

airlineIDToCountryString = dict()
airlineIDToNameString = dict()
for row in csv.reader(open("airlines.dat", "rb"), delimiter=","): # col 0 id ID
    airlineIDToCountryString[int(row[0])] = row[6]
    airlineIDToNameString[int(row[0])] = row[2]
    
airportIDToCountryString = dict()
airportIDToNameString = dict()
airportIDToLatLong = dict()
for row in csv.reader(open("airports.dat", "rb"), delimiter=","): # col 3 is country string, col 0 is ID
    airportIDToCountryString[int(row[0])] = row[3]
    airportIDToNameString[int(row[0])] = row[4]
    airportIDToLatLong[int(row[0])] = (float(row[6]), float(row[7]))


def printFifthFreedoms(fifthFreedoms):
    for ii in xrange(0, len(fifthFreedoms)):
        srcID = fifthFreedoms[ii][0]
        destID = fifthFreedoms[ii][1]
        airlineID = fifthFreedoms[ii][2]
        if "\N" in airlineIDToNameString[airlineID]:
            continue
        distance = haversine(airportIDToLatLong[srcID], airportIDToLatLong[destID])
        print "Found 5th freedom: " + airportIDToNameString[srcID]+" ("+airportIDToCountryString[srcID]+")" + " -> " + airportIDToNameString[destID]+" ("+airportIDToCountryString[destID]+")" + " ("+str(int(round(distance)))+" km)" + \
        " on airline "+airlineIDToNameString[airlineID]+" from "+airlineIDToCountryString[airlineID]


    
fifthFreedoms = list()
for row in csv.reader(open("routes.dat", "rb"), delimiter=","):
    if "\N" in row[3] or "\N" in row[5] or "\N" in row[1]:
        continue
    srcID = int(row[3])
    destID = int(row[5])
    airlineID = int(row[1])
    if airportIDToCountryString[srcID] != airportIDToCountryString[destID]: # intl flight
        if airlineIDToCountryString[airlineID] != airportIDToCountryString[srcID]: # airline not from src country
            if airlineIDToCountryString[airlineID] != airportIDToCountryString[destID]: # airline not from dest country
                distance = haversine(airportIDToLatLong[srcID], airportIDToLatLong[destID])
                #print distance
                fifthFreedoms.append( (srcID, destID, airlineID, distance) )
                #is 5th freedom!
                #print "Found 5th freedom: " + airportIDToNameString[srcID] + " -> " + airportIDToNameString[destID] + " ("+str(round(distance))+" km)"
fifthFreedoms.sort(key=lambda x: x[3])
printFifthFreedoms(fifthFreedoms)
