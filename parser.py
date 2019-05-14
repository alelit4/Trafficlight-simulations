import xml.etree.ElementTree as ET
root = ET.parse('fulldata.xml').getroot()


for step in root.iter('data'):
   print("--> " + str(step.attrib["timestep"]))
   trafficlights = step.find('tls')
   #for tl in trafficlights.iter('trafficlight'):
   #   print(" " + str(tl.attrib["state"]))
   trafficlightState = trafficlights[0].attrib["state"][0]  # rGrG state
   # print(" " + trafficlightState)
   vehicles = step.find('vehicles')
   contVehicles = 1
   for vehicle in vehicles.iter('vehicle'):
      pos = float(vehicle.attrib["y"])
      id = vehicle.attrib["id"]
      # and (pos > 500) and (pos < 518) ):
      if(trafficlightState == "r"):
         #print('--->> ROJO! ')
         if (pos > 500) and (pos < 520):
            print("----->> pos < 500 and > 520 ! ")
            print( str(id) + " -> pos = " + str(pos) )
            #   print(" " + str(contVehicles) + ') y=' + pos + ' speed= ' + str(vehicle.attrib["speed"]))
      contVehicles += 1
   
   
