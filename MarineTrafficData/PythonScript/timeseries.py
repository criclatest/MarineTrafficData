
from osgeo import ogr
from datetime import datetime
import json
import os

dafile = [r"Zone19_2009_01.gdb",r"Zone19_2009_03.gdb",r"Zone19_2009_04.gdb",r"Zone19_2009_05.gdb",r"Zone19_2009_06.gdb",r"Zone19_2009_07.gdb",r"Zone19_2009_08.gdb",r"Zone19_2009_09.gdb",r"Zone19_2009_10.gdb",r"Zone19_2009_11.gdb",r"Zone19_2009_12.gdb"]
months = ['Jan','March','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']


region = ['2','3','4','5','6','7']
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
	#layer.SetAttributeFilter("VoyageId = 1")


	broadcastDict = dict()
	cnt = 0
	c = 0
	for feature in layer:
		geom = feature.GetGeometryRef()
		mmsi = feature['MMSI']
		vId = months[monthIndex] + '_' + str(feature['VoyageID'])
		#print vId
		if vId in voyageDict:
			if mmsi not in broadcastDict:
				broadcastDict[mmsi] = dict()
				broadcastDict[mmsi][vId] = [{'SOG' : feature['SOG'], 'DateTime' : feature['BaseDateTime']}]
			else:
				if vId not in broadcastDict[mmsi]:
					broadcastDict[mmsi][vId] = [{'SOG' : feature['SOG'], 'DateTime' : feature['BaseDateTime']}]
				else:
					broadcastDict[mmsi][vId].append({'SOG' : feature['SOG'], 'DateTime' : feature['BaseDateTime']})
		else:
			cnt = cnt + 1


	#a = int(datetime.strptime("2013-5-4 00:00:00", "%Y-%m-%d %H:%M:%S").strftime('%s')) * 1000
	#print a

	menuJson = []
	for mmsi in broadcastDict:
		path ="/Users/nilesh/Project/timeseries/"
		voyages = []
		for vId in broadcastDict[mmsi]:
			#sogDateTime = ""
			sogDateTime = []
			for rec in broadcastDict[mmsi][vId]:
				#d = datetime.strptime(rec['DateTime'], '%Y/%m/%d %H:%M:%S')
				d =((datetime.strptime(rec['DateTime'], '%Y/%m/%d %H:%M:%S'))-datetime(1970,1,1)).total_seconds()*1000
				#d = int(datetime.strptime(rec['DateTime'], '%Y/%m/%d %H:%M:%S').strftime('%s')) * 1000
				#temp = '[Date.UTC'+'(' + str(d.year) + "," + str(d.month) + "," + str(d.day) + "," + str(d.hour) + "," + str(d.minute) + "," + str(d.second)+"),"+ str(rec['SOG'])+'],'
				#temp.replace("\"", "")
				#temp = [(d.year,d.month,d.day,d.hour,d.minute,d.second,rec['SOG'])]
				#sogDateTime = sogDateTime + temp
				sogDateTime.append([d, rec['SOG']])
			with open(path+str(vId)+'_timeseries.json', 'w') as outfile:
				json.dump(sogDateTime, outfile)

	monthIndex = monthIndex + 1

#End For Loop