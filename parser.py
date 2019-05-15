import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt


isDebugging = False # if it is debugging the program is verbose 
infringingVehicles = [] # The list of all infractors 
allIDataInfringingVehicles = {}
# The reference of limits is based on the location of the juction
upperLimitJunction = 500 
lowerLimitJunction = 520

def getJsonVehicle(vehicle, step):
   return {'step' : step, 'speed' : vehicle.attrib["speed"], 'pos' : float(vehicle.attrib["y"]) } 

def startParser(infringingVehicles, allIDataInfringingVehicles):
   root = ET.parse('fulldata.xml').getroot()

   for step in root.iter('data'):
      trafficlights = step.find('tls')
      trafficlightState = trafficlights[0].attrib["state"][0]  # rGrG state
      allVehiclesInStep = step.find('vehicles')
      vehiclesInStep = 1
      for vehicle in allVehiclesInStep.iter('vehicle'):
         locationY = float(vehicle.attrib["y"])
         currentVehicleId = vehicle.attrib["id"]
         if(trafficlightState == "r") and ('down' in currentVehicleId):
            if (locationY > upperLimitJunction) and (locationY < lowerLimitJunction):
               if isDebugging:
                  print('Step %s ----->> Trafficlight Infraction!' % step.attrib["timestep"])
                  print( '%s -> pos = %i' % (currentVehicleId, locationY))
               if currentVehicleId not in infringingVehicles:
                  infringingVehicles.append(currentVehicleId)
                  allIDataInfringingVehicles[currentVehicleId] = []
               allIDataInfringingVehicles[currentVehicleId].append(getJsonVehicle(vehicle, step.attrib["timestep"])) 
         vehiclesInStep += 1
   
def printInfo(infringingVehicles, allIDataInfringingVehicles):
   print('There are %i/1000 tlv' % len(infringingVehicles) )
   print(' '.join(infringingVehicles)) 
   print('--------------------------------------')
   print(allIDataInfringingVehicles)
   for id, vehicleData in sorted(allIDataInfringingVehicles.items()):
      print('Vehicle (%s) route = %s' % (id, vehicleData))
    
def getBasicPlot(infringingVehicles):
   plt.plot(range(0, len(infringingVehicles)), range(0, len(infringingVehicles)))
   plt.ylabel('some numbers')
   plt.show()

if __name__ == "__main__":
   startParser(infringingVehicles, allIDataInfringingVehicles)
   printInfo(infringingVehicles, allIDataInfringingVehicles) if isDebugging else 0