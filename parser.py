import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy
import json

isDebugging = False  # if it is debugging the program is verbose
infringingVehicles = []  # The list of all infractors
allDataInfringingVehicles = {}
allDataVehicles = {}
# The reference of limits is based on the location of the juction
upperLimitJunction = 500
lowerLimitJunction = 520


def getJsonVehicle(vehicle, step):
	return {'step': step, 'speed': vehicle.attrib["speed"], 'pos': float(vehicle.attrib["y"])}

def startParserFCD(infringingVehicles, allDataInfringingVehicles):
	root = ET.parse('sumofcdoutput.xml').getroot()
	for step in root.iter('timestep'):
		for vehicle in step.iter('vehicle'):
			locationY = float(vehicle.attrib["y"])
			currentVehicleId = vehicle.attrib["id"]
			if ('down' in currentVehicleId):
				if currentVehicleId not in infringingVehicles:
					infringingVehicles.append(currentVehicleId)
					allDataInfringingVehicles[currentVehicleId] = []
				allDataInfringingVehicles[currentVehicleId].append(getJsonVehicle(vehicle, step.attrib["time"]))
				if currentVehicleId not in allDataVehicles.keys():
					allDataVehicles[currentVehicleId] = []
				allDataVehicles[currentVehicleId].append(getJsonVehicle(vehicle, step.attrib["time"]))

def startParserFullData(infringingVehicles, allDataInfringingVehicles):
	root = ET.parse('fulldata.xml').getroot()
	for step in root.iter('data'):
		trafficlights = step.find('tls')
		trafficlightState = trafficlights[0].attrib["state"][0]  # rGrG state
		allVehiclesInStep = step.find('vehicles')
		vehiclesInStep = 1
		for vehicle in allVehiclesInStep.iter('vehicle'):
			locationY = float(vehicle.attrib["y"])
			currentVehicleId = vehicle.attrib["id"]
			if ('down' in currentVehicleId):
				if (trafficlightState == "r"):
					if (locationY > upperLimitJunction) and (locationY < lowerLimitJunction):
						if isDebugging:
							print('Step %s ----->> Trafficlight Infraction!' % step.attrib["timestep"])
							print('%s -> pos = %i' % (currentVehicleId, locationY))
						if currentVehicleId not in infringingVehicles:
							infringingVehicles.append(currentVehicleId)
							allDataInfringingVehicles[currentVehicleId] = []
						allDataInfringingVehicles[currentVehicleId].append(getJsonVehicle(vehicle, step.attrib["timestep"]))
				vehiclesInStep += 1
				if currentVehicleId not in allDataVehicles.keys():
					allDataVehicles[currentVehicleId] = []
				allDataVehicles[currentVehicleId].append(getJsonVehicle(vehicle, step.attrib["timestep"]))


def printInfo(infringingVehicles, allIDataInfringingVehicles):
	print('There are %i/1000 tlv' % len(infringingVehicles))
	print(' '.join(infringingVehicles))
	print('--------------------------------------')
	print(allIDataInfringingVehicles)
	for id, vehicleData in sorted(allIDataInfringingVehicles.items()):
		print('Vehicle (%s) route = %s' % (id, vehicleData))


def getBasicPlot(infringingVehicles):
	plt.plot(range(0, len(infringingVehicles)), range(0, len(infringingVehicles)))
	plt.ylabel('some numbers')
	plt.show()


def getVehiclePlot(vehicle):
	print('-------------------------------')
	print('%s' % vehicle)
	print('-------------------------------')
	lists = sorted(vehicle, key=lambda k: k['step'])  # sorted by key, return a list of tuples
	print('%s' % lists)


def printAllRoutes(vehicles):
	for vehicle in vehicles:
		print('-------------------------------')
		print('-> %s:' % (vehicle) )
		print('      %s' % vehicles[vehicle])
		print('-------------------------------')

def printRoutes(vehicles):
	for vehicle in vehicles:
		print('-------------------------------')
		print('-> Vehicle %s:' % (vehicle) )
		for step in vehicles[vehicle]:
			print('    pos = %s - vel = %s' % (step['pos'], step['speed']))
		print('-------------------------------')

def printRoutesPoints(vehicles):
	for vehicle in vehicles:
		print('-------------------------------')
		print('-> Vehicle %s:' % (vehicle) )
		for step in vehicles[vehicle]:
			print(' %s ' % step)
		print('-------------------------------')

def saveRoutesPoints(vehicles, fileName="tlsredbadbehaviour.txt"):
	file = open(fileName, 'w')
	for vehicle in vehicles:
		# print('%s' % (vehicle) ),
		for step in vehicles[vehicle]:
			print(' %s ' % step),
			file.write(' %s ' % step),
		print('')
		file.write('\n'),
	file.close()


def getAllRoutesVehicles(allDataVehicles, infringingVehicles):
	routeInfringingVehicles = {}
	for vehicle in allDataVehicles:
		if vehicle in infringingVehicles:
			routeInfringingVehicles[vehicle] = allDataVehicles.get(vehicle)
	if isDebugging:
		print('infringingVehicles %d ' % len(infringingVehicles))
		print('routeInfringingVehicles %d ' % len(routeInfringingVehicles.keys()))
	return  routeInfringingVehicles


def getNearPositionData(point, vehicle, range = 0.5):
	nearStep = 0
	for step in vehicle:
		if ((step['pos'] > point - range) and (step['pos'] < point + range)):
			nearStep = step
	if (nearStep == 0):
		return getNearPositionData(point, vehicle, 1)
	return nearStep['speed']

def getPointsRoutes(routeInfringingVehicles):
	points = numpy.arange(505, 556, 5)
	vehiclePoints = {}
	for vehicle in routeInfringingVehicles:
	 	vehiclePoints[vehicle] = [];
	 	for point in points:
	 		vehiclePoints[vehicle].append(getNearPositionData(point, routeInfringingVehicles[vehicle]) )
	return vehiclePoints

if __name__ == "__main__":
	startParserFCD(infringingVehicles, allDataInfringingVehicles)
	printInfo(infringingVehicles, allDataInfringingVehicles) if isDebugging else 0
 	routeInfringingVehicles = getAllRoutesVehicles(allDataVehicles, infringingVehicles)
	printRoutes(routeInfringingVehicles) if isDebugging else 0
	vehiclesPoints = getPointsRoutes(routeInfringingVehicles)
	# printRoutesPoints(vehiclesPoints)
	saveRoutesPoints(vehiclesPoints)
