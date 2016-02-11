from osgeo import ogr
from datetime import datetime
import json
import os
import time



dafile = [r"Zone19_2009_01.gdb",r"Zone19_2009_03.gdb",r"Zone19_2009_04.gdb",r"Zone19_2009_05.gdb",r"Zone19_2009_06.gdb",r"Zone19_2009_07.gdb",r"Zone19_2009_08.gdb",r"Zone19_2009_09.gdb",r"Zone19_2009_10.gdb",r"Zone19_2009_11.gdb",r"Zone19_2009_12.gdb"]
months = ['Jan','March','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

region = ['2','3','4','5','6','7']

regionCode = dict()
regionCode['2']='Europe'
regionCode['3']='North and Central America and Caribbean'
regionCode['4']='Asia'
regionCode['5']='Oceania'
regionCode['6']='Africa'
regionCode['7']='South America'

monthIndex = 0

with open('mids.json') as data_file:    
    data = json.load(data_file)

for gdbFile in dafile:
	print months[monthIndex]
	dataSource = ogr.Open(gdbFile)
	layer = dataSource.GetLayer("Vessel")

	cnt = 0

	vesselDict = dict()

	for feature in layer:
		#print len(str(feature['MMSI']))
		if len(str(feature['MMSI'])) == 9:
			#print str(feature['MMSI'])[0]
			if str(feature['MMSI'])[0] in region:
				if str(feature['MMSI'])[0:3] in data:
					if feature['MMSI'] not in vesselDict:
						cnt = cnt + 1
						vesselDict[feature['MMSI']] = feature
					elif vesselDict[feature['MMSI']]['IMO'] == 0 or len(vesselDict[feature['MMSI']]['Name'].strip()) == 0:#If 2 record prsent for same voyages the pick up valid data
						cnt = cnt + 1
						vesselDict[feature['MMSI']] = feature

	dataSource = ogr.Open(gdbFile)
	layer = dataSource.GetLayer("Voyage")
	cnt  = 0

	voyageDict = dict()

	for feature in layer:
		vId = months[monthIndex] + '_' + str(feature['VoyageID'])
		if feature['MMSI'] in vesselDict:
			if vId in voyageDict:
				try:
					if datetime.strptime(feature['StartTime'], '%Y/%m/%d %H:%M:%S') > datetime.strptime(voyageDict[vId]['StartTime'], '%Y/%m/%d %H:%M:%S'):
						voyageDict[vId] = feature
				except Exception:
					print 'Exception Voyage layer : '+ str(vId)
			else:
				cnt = cnt + 1
				voyageDict[vId] = feature

	dataSource = ogr.Open(gdbFile)
	layer = dataSource.GetLayer("Broadcast")
	#layer.SetAttributeFilter("VoyageId in (1)")
	fmt = '%Y/%m/%d %H:%M:%S'
	broadcastDict = dict()

	for feature in layer:
		geom = feature.GetGeometryRef()
		mmsi = feature['MMSI']
		vId = months[monthIndex] + '_' + str(feature['VoyageID'])
		if vId in voyageDict:
			#print vId
			if mmsi not in broadcastDict:
				broadcastDict[mmsi] = dict()
				broadcastDict[mmsi][vId] = {'Distance' : 0, 'prevTime' : feature['BaseDateTime']}
			else:
				if vId not in broadcastDict[mmsi]:
					broadcastDict[mmsi][vId] = {'Distance' : 0, 'prevTime' : feature['BaseDateTime']}
				else:
					d2 = datetime.strptime(feature['BaseDateTime'], fmt)
					d1 = datetime.strptime(broadcastDict[mmsi][vId]['prevTime'], fmt)
					d1_ts = time.mktime(d1.timetuple())
					d2_ts = time.mktime(d2.timetuple())
					broadcastDict[mmsi][vId]['Distance'] = broadcastDict[mmsi][vId]['Distance'] + ((feature['SOG'] * 1.151 * int(d2_ts-d1_ts)) / (60 * 60))
					broadcastDict[mmsi][vId]['prevTime'] = feature['BaseDateTime']

	path ="/Users/nilesh/Project/VoyageVesselDetail/"

	for mmsi in broadcastDict:
		country =  ''
		ko = str(mmsi)[:1]
		#print str(ko) + ' : ' + str(mmsi)
		if ko in regionCode:
			country = regionCode[ko]
			#print country
		for vId in broadcastDict[mmsi]:
			#print vId
			with open(path+str(vId)+'_details.json', 'w') as outfile:
				#print format(broadcastDict[mmsi][vId]['Distance'], '.2f')
				#json.dump({'IMO' : vesselDict[mmsi]['IMO'], 'CallSign' : vesselDict[mmsi]['CallSign'], 'Width' : vesselDict[mmsi]['Width'],'DimensionComponents' : vesselDict[mmsi]['DimensionComponents'],'MMSI' : mmsi,'Name' : vesselDict[mmsi]['Name'],'Type' : vesselDict[mmsi]['VesselType'],'Destination' : voyageDict[vId]['Destination'],'Cargo' : voyageDict[vId]['Cargo'],'ETA' : voyageDict[vId]['ETA'],'StartTime' : voyageDict[vId]['StartTime'],'EndTime' : voyageDict[vId]['EndTime'], 'Draught' : vesselDict[mmsi]['Draught']}, outfile)
				json.dump({'country' : country, 'Distance': format(broadcastDict[mmsi][vId]['Distance'], '.2f'),'IMO' : vesselDict[mmsi]['IMO'], 'CallSign' : vesselDict[mmsi]['CallSign'], 'Width' : vesselDict[mmsi]['Width'],'DimensionComponents' : vesselDict[mmsi]['DimensionComponents'],'MMSI' : mmsi,'Name' : vesselDict[mmsi]['Name'],'Type' : vesselDict[mmsi]['VesselType'],'Destination' : voyageDict[vId]['Destination'],'Cargo' : voyageDict[vId]['Cargo'],'ETA' : voyageDict[vId]['ETA'],'StartTime' : voyageDict[vId]['StartTime'],'EndTime' : voyageDict[vId]['EndTime'], 'Draught' : voyageDict[vId]['Draught']},outfile)

	monthIndex = monthIndex + 1			
##End For Loop