import xml.etree.ElementTree as ET
root = ET.parse('fulldata.xml').getroot()

isDebugging = True # if it is debugging the program is verbose 
infringingVehicles = [] # The list of all infractors 

# The reference of limits is based on the location of the juction
upperLimitJunction = 500 
lowerLimitJunction = 520

for step in root.iter('data'):

   trafficlights = step.find('tls')
   # Too see the state of the junction
   #for tl in trafficlights.iter('trafficlight'):
   #   print(" " + str(tl.attrib["state"]))
   
   trafficlightState = trafficlights[0].attrib["state"][0]  # rGrG state
   allVehiclesInStep = step.find('vehicles')
   vehiclesInStep = 1
   for vehicle in allVehiclesInStep.iter('vehicle'):
      locationY = float(vehicle.attrib["y"])
      currentVehicleId = vehicle.attrib["id"]
      if(trafficlightState == "r"):
         if (locationY > upperLimitJunction) and (locationY < lowerLimitJunction):
            if isDebugging:
               print('Step %s ----->> Trafficlight Infraction!' % step.attrib["timestep"])
               print( '%s -> pos = %i' % (currentVehicleId, locationY))
            if currentVehicleId not in infringingVehicles:
               infringingVehicles.append(currentVehicleId)
      vehiclesInStep += 1
   
print('There are %i/1000 tlv' % len(infringingVehicles) )
print(' '.join(infringingVehicles)) if isDebugging else 0
