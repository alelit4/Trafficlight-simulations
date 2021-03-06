import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy
import json


isDebugging = False  # if it is debugging the program is verbose
infringingVehicles = []  # The list of all infractors
noInfringingVehicles = []  # The list of good dirvers
allDataInfringingVehicles = {}
allDataNoInfringingVehicles = {}
allDataVehicles = {}

# The reference of limits is based on the location of the juction
upperLimitJunction = 500
lowerLimitJunction = 520

def getJsonVehicle(vehicle, step):
	return {'step': step, 'speed': vehicle.attrib["speed"], 'pos': float(vehicle.attrib["y"])}

# FCD is where bad behaviour was simulated
def startParserFCD(infringingVehicles, allDataInfringingVehicles, file="sumofcdoutput.xml"):
	root = ET.parse(file).getroot()
	for step in root.iter('timestep'):
		for vehicle in step.iter('vehicle'):
			currentVehicleId = vehicle.attrib["id"]
			if ('down' in currentVehicleId):
				if currentVehicleId not in infringingVehicles:
					infringingVehicles.append(currentVehicleId)
					allDataInfringingVehicles[currentVehicleId] = []
				allDataInfringingVehicles[currentVehicleId].append(getJsonVehicle(vehicle, step.attrib["time"]))
				if currentVehicleId not in allDataVehicles.keys():
					allDataVehicles[currentVehicleId] = []
				allDataVehicles[currentVehicleId].append(getJsonVehicle(vehicle, step.attrib["time"]))

def startParserFullData(infringingVehicles, allDataInfringingVehicles, file='fulldata.xml'):
	root = ET.parse(file).getroot()
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
			print(' %s ' % step),
		print('\n-------------------------------')

def saveRoutesPoints(vehicles, fileName="tlsredbadbehaviour.txt", label=1):
	file = open(fileName, 'w')
	points = numpy.arange(505.0, 556.0, 5)
	file.write('0 '),
	for point in points:
		print('%s ' % point),
		file.write('%s ' % point),
	print('')
	file.write('\n'),
	for vehicle in vehicles:
		# print('%s' % (vehicle) ),
		file.write('%s ' % label)
		for step in vehicles[vehicle]:
			print('%s ' % step),
			file.write('%s ' % step)
		print('')
		file.write('\n'),
	file.close()


def getAllRoutesVehicles(allDataVehicles, idVehicles):
	routeSelectedVehicles = {}
	for vehicle in allDataVehicles:
		if vehicle in idVehicles:
			routeSelectedVehicles[vehicle] = allDataVehicles.get(vehicle)
	if isDebugging:
		print('idVehicles %d ' % len(idVehicles))
		print('routeSelectedVehicles %d ' % len(routeSelectedVehicles.keys()))
	return  routeSelectedVehicles

# To simplify the parser, the returned value is just the speed
def getNearPositionData(point, vehicle, range = 1):
	nearStep = 0
	for step in vehicle:
		if ((step['pos'] > point - range) and (step['pos'] < point + range)):
			nearStep = step
	if (nearStep == 0):
		nearStep = getNearPositionData(point, vehicle, range+1)
	return nearStep

def getPointsRoutes(routeInfringingVehicles):
	points = numpy.arange(505, 556, 5)
	vehiclePoints = {}
	for vehicle in routeInfringingVehicles:
		vehiclePoints[vehicle] = [];
		for point in points:
			vehiclePoints[vehicle].append(getNearPositionData(point, routeInfringingVehicles[vehicle])['speed'] )
	return vehiclePoints

def cleanVariables():
	allDataVehicles = {}
	infringingVehicles = []  # The list of all infractors
	noInfringingVehicles = []  # The list of good dirvers
	allDataInfringingVehicles = {}
	allDataNoInfringingVehicles = {}


if __name__ == "__main__":
	# FCD is used to BB
	# BAD BEHAVIOUR
	print('\n\nBAD BEHAVIOUR ')
	for i in range(1, 11):
		cleanVariables()
		file = "simulations/sumofcdoutput1000_%s.xml" % i
		print('\n\n ---> Parsing BAD BEHAVIOUR of file %s' % file)
		startParserFCD(infringingVehicles, allDataInfringingVehicles, file)
		routeInfringingVehicles = getAllRoutesVehicles(allDataVehicles, infringingVehicles)
		# printRoutes(routeInfringingVehicles) if isDebugging else 0
		vehiclesPoints = getPointsRoutes(routeInfringingVehicles)
		# printRoutesPoints(vehiclesPoints) if isDebugging else 0
		saveRoutesPoints(vehiclesPoints, "output/tlsredbadbehaviour1000_%s.txt" % i)

	# GOOD BEHAVIOUR
	print('\n\nGOOD BEHAVIOUR ')
	for i in range(1, 11):
		cleanVariables()
		file = "simulations/fulldata1000_%s.xml" % i
		print('\n\n ---> Parsing GOOD BEHAVIOUR of file %s' % file)
		startParserFullData(noInfringingVehicles, allDataNoInfringingVehicles, file)
		# printInfo(noInfringingVehicles, allDataNoInfringingVehicles) if isDebugging else 0
		routeGoodVehicles = getAllRoutesVehicles(allDataVehicles, noInfringingVehicles)
		# printRoutes(routeGoodVehicles) if isDebugging else 0
		vehiclesPoints = getPointsRoutes(routeGoodVehicles)
		# printRoutesPoints(vehiclesPoints) if isDebugging else 0
		saveRoutesPoints(vehiclesPoints, "output/tlsredgoodbehaviour1000_%s.txt" % i, 0)
