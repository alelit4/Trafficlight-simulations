import xml.etree.ElementTree as ET
root = ET.parse('fulldata.xml').getroot()

contViolations = 1
infringingVehicles = []

for step in root.iter('data'):
   #print("--> " + str(step.attrib["timestep"]))
   trafficlights = step.find('tls')
   # Too see the state of the junction
   #for tl in trafficlights.iter('trafficlight'):
   #   print(" " + str(tl.attrib["state"]))
   trafficlightState = trafficlights[0].attrib["state"][0]  # rGrG state
   # print(" " + trafficlightState)
   vehicles = step.find('vehicles')
   contVehicles = 1
   for vehicle in vehicles.iter('vehicle'):
      pos = float(vehicle.attrib["y"])
      id = vehicle.attrib["id"]
      if(trafficlightState == "r"):
         #print('--->> ROJO! ')
         if (pos > 500) and (pos < 520):
            print('Step %s ----->> TL Violation!' % step.attrib["timestep"] )
            contViolations+=1
            print( str(id) + " -> pos = " + str(pos) )
            if id not in infringingVehicles: 
               infringingVehicles.append(id)
            #   print(" " + str(contVehicles) + ') y=' + pos + ' speed= ' + str(vehicle.attrib["speed"]))
      contVehicles += 1
   
print("There are " + str(len(infringingVehicles)) + " tlv")
print(infringingVehicles)
