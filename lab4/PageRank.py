#!/usr/bin/python

from random import randint
import time
import sys
import operator
import matplotlib.pyplot as plt


# Edge: each edge has the origin code of an airport and its weight.
class Edge:
    def __init__ (self, origin = None, index = None):
        self.origin = origin
        self.weight = 1.0				# how many times there's a route from origin to an specific airport
        self.index = index 				# Index for airportList

    def __repr__(self):
        return "edge: {0} {1}".format(self.origin, self.weight)

class Airport:
    def __init__ (self, iden=None, name=None, index = None):
        self.code = iden				# IATA code
        self.name = name 				# Name of the airport
        self.routes = []				        # list of edges of the airports that have this airport as destination; list[edges]
        self.routeHash = dict()			# dict{key = airport IATA code : index in routes}
        self.outweight = 0.0			# weight from this airport to others
        self.index = index

    def __repr__(self):
        return "{0}\t{2}\t{1}".format(self.code, self.name, self.pageIndex)


def nuevaRuta(aeroport, codiOrigen):
    if codiOrigen in aeroport.routeHash:
        index = aeroport.routeHash[codiOrigen]
        edge = aeroport.routes[index]
        edge.weight += 1.0
    else:
        pos = airportHash[codiOrigen].index
        edge = Edge(codiOrigen, pos)

        aeroport.routes.append(edge)
        index = len(aeroport.routes) - 1
        aeroport.routeHash[codiOrigen] = index




#edgeList = [] # list of Edges
#edgeHash = dict() # hash of edge to ease the match
airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport
routeList = []
routeHash = dict()
pageR = []


def readAirports(fd):
    print("Reading Airport file from {0}".format(fd))
    airportsTxt = open(fd, "r");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 :  # Is this OK????! != 5?!?!?!
                raise Exception('not an IATA code')
            a.name = temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code = temp[4][1:-1]
            a.index = cont
        except Exception as inst:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()
    print ("There were {0} Airports with IATA code".format(cont))


# Reads routes and writes it into the airports
def readRoutes(fd):
    # airline code, op airline code, origin airport code, op origin code, 
    # dest airport code, op destination airport code
    # only IATA codes
    
    print ("Reading Routes file from {0}".format(fd))
    routesTxt = open(fd, "r");
    cont = 0
    for line in routesTxt.readlines():
        try: 
            temp = line.split(',')
            if len(temp[2]) != 3 or len(temp[4]) != 3:
                raise Exception('not an IATA code')
            
            codigoOrigen = temp[2]
            codigoDestino = temp[4]
            
        
            if not(codigoOrigen in airportHash):
                raise Exception ("No se ha encontrado el aeropuerto de Origen")
            else:
                idxOrigen = airportHash[codigoOrigen].index
                airpOrigen = airportList[idxOrigen]
            if not(codigoDestino in airportHash):
                raise Exception ("No se ha encontrado el aeropuerto de Destino")
            else:
                idxDesti = airportHash[codigoDestino].index
                airpDesti = airportList[idxDesti]
           
            nuevaRuta(airpDesti, codigoOrigen)
            airpOrigen.outweight += 1.0
        
        except Exception as inst:
            pass
        else:
            cont += 1
            
    routesTxt.close()
    print ("There were {0} Airports with IATA code".format(cont))
 
 
def checkSum1(vect):
    print (sum(vect))

def computePageRanks(alfa):        
        print( "Computing Page Rank")
        
        n = len(airportList)
        P = [1.0/n]*n
        
        iters = 0
        stop = False
        sinkNodes = len(list(filter(lambda n: n.outweight == 0, airportList)))
        
        aux = 1.0/n
        L1 = (1.0 - alfa)/n
        
        numberOuts = alfa/float(n)*sinkNodes
        
        while not stop:
            Q = [0.0]*n
            
            for i in range(n):
                    airp = airportList[i]
                    suma = 0
                    
                    for edge in airp.routes:
                        w = edge.weight
                        out = airportList[edge.index].outweight
                        suma += P[edge.index] * w / out 
                        
                    Q[i] = alfa * suma + L1 + aux*numberOuts
            
            aux = L1 + aux*numberOuts
            
            
            # print(f'IteraciÃ³ {iters} : Aux: {aux}')
            
            val = [a_i - b_i for a_i, b_i in zip(P, Q)] 
            
            absolut = map(lambda v: abs(v), val)
            
            stop = all(map(lambda v: v < 1 * 10**(-15), absolut)) or iters==2000
            print(iters)
            P = Q
            iters += 1
        
        global pageR
        pageR = P
        return iters
     

# Print( list of airports
def outputPageRanks():
    
    print( " ******************************************************************************* ")
    print( " ********************** ( Page rank, Airport name) ***************************** ")
    print( " ******************************************************************************* ")
    
    n = len(airportList)
    myList = {key : p for key, p in zip(range(n) ,pageR)}
    #print( myList

    # sort descending myList
    myNewList = sorted(myList.items(), key=operator.itemgetter(1), reverse=True)

    index = 1
    print( "Airports sorted by PageRank:")
    for airp, page in myNewList:
        name = airportList[airp].name
        code = airportList[airp].code
        #print(  "%s. %s [%s], PageRank = %s"%(index, name, code, page)
        print( "(%s, %s)" %(page, name))
        index += 1



def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")

    time1 = time.time()
    iterations = computePageRanks(0.85)
    time2 = time.time()
    outputPageRanks()
    
    s = sum(pageR)
    
    print( "Sum of Page Rank: %s" %(s))
    print( "#Iterations:", iterations)
    print( "Time of computePageRanks():", time2-time1)
    readAirports("airports.txt")
    readRoutes("routes.txt")
    
    alfa = 1
    niters = []
    alfas = []
    while alfa > 0.5:
    	print("a")
    	iterations=computePageRanks(alfa)
    	if (iterations!=2000):
	    	niters.append(computePageRanks(alfa))
	    	alfas.append(alfa)
    	alfa -= 0.1
    	print("Alfa vale: ", alfa)
    plt.plot(alfas, niters)
    plt.xlabel('ALFA')
    plt.ylabel('ITER')
    plt.show()
    
    
    
    
     



if __name__ == "__main__":
    sys.exit(main())
