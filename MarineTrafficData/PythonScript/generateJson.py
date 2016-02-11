from osgeo import ogr
from datetime import datetime
import json
import os
import collections

dafile = [r"Zone19_2009_01.gdb",r"Zone19_2009_02.gdb",r"Zone19_2009_03.gdb",r"Zone19_2009_04.gdb",r"Zone19_2009_05.gdb",r"Zone19_2009_06.gdb",r"Zone19_2009_07.gdb",r"Zone19_2009_08.gdb",r"Zone19_2009_09.gdb",r"Zone19_2009_10.gdb",r"Zone19_2009_11.gdb",r"Zone19_2009_12.gdb"]
months = ['Jan','Feb','March','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
monthsLower = ['jan','feb','march','apr','may','jun','jul','aug','sep','oct','nov','dec']
#dafile = [r"Zone19_2009_10.gdb"]
#monthsLower = ['oct']
#months = ['Oct']

with open('mids.json') as data_file:    
    data = json.load(data_file)

region = ['2','3','4','5','6','7']
monthIndex = 0
dest = dict()
allMenuJson = []
globalBroadcast = dict()

for gdbFile in dafile:
	print months[monthIndex]
	dataSource = ogr.Open(gdbFile)
	layer = dataSource.GetLayer("Vessel")
	#layer.SetAttributeFilter("VoyageId in (1)")

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
	#layer.SetAttributeFilter("VoyageId in (1)")
	cnt  = 0

	voyageDict = dict()

	#b = datetime.strptime('2009/01/02 22:53:10', '%Y/%m/%d %H:%M:%S')

	#print a > b

	for feature in layer:
		if feature['MMSI'] in vesselDict:
			vId = months[monthIndex] + '_' + str(feature['VoyageID'])
			if vId in voyageDict:
				try:
					if datetime.strptime(feature['StartTime'], '%Y/%m/%d %H:%M:%S') > datetime.strptime(voyageDict[vId]['StartTime'], '%Y/%m/%d %H:%M:%S'):
						voyageDict[vId] = feature
				except Exception:
					print 'Exception Voyage layer : '+ str(vId)
			else:
				cnt = cnt + 1
				voyageDict[vId] = feature

	#print cnt

	dataSource = ogr.Open(gdbFile)
	layer = dataSource.GetLayer("Broadcast")
	##Addd here
	##--January---
	if monthIndex == 0:
		layer.SetAttributeFilter("VoyageId not in (39,86294,11036,66923,68299,79432,54113,3568,108429,32779,32779,101575,80427,36730,20422,3536,3185,76177,40398,102,3543,54848,15725,44235,112342,29519,25334,14747,108566,59455,91805,45989,20472,7002,67808,44237,14901,43608,72298,50780,36937,146,20442,11014,40400,6200,33023,51703,81278,3,36922,48070,104388,39725,81247,94582)")
	#feb---
	elif monthIndex == 1:
		layer.SetAttributeFilter("VoyageId not in (69608,55934,57462,47146,22575,45581,55778,49896,160,83652,68723,50545,56930,47157,11664,10999,44721,35,65647,44571,39530,30629,24473,62679,78732,54415,16745,11653,72784,48506,76262,66201,32634,82279,36677,77554,4122,78889,41,64023,85148,3765,69055,24774,46837,4141,26502,14901,26000,1735,6460,17087,8170,28235,50984,78239,14946,44560,13628,46712,18421,51879,86817,18403,65598,79291,34548,49755,6562,49900,71522,53,2,6486,11660,18022,14927,30641,81334,72772,40380,61799,39176,17,4,20,26486,48895, 59327,67427)")
	#---March---
	elif monthIndex == 2:
		layer.SetAttributeFilter("VoyageId not in (29063,16723,21579,80077,24485,28695,27507,16729,9422,74211,50895,12478,27405,74794,16048,77997,80241,21566,12095,9445,9453,6704,103,51179,30847,24485,26002,23851,24491,17925,61339,29059,60466,1987,36672,24039,6687,61198,18684,21560,41778,68722,17,28900,21519,16068,6393,3541,38055,3538,22827,20,6,31521,56,85072,72126, 63, 26983,28918,170,170,116,75808,18446,18446,16703,16703,29054,9417,24506,19,26956,22888,34760,56528,39,48151)")
	#--April--
	elif monthIndex == 3:
		layer.SetAttributeFilter("VoyageId not in (151,23210,76203,22,83171,73368,38415,64215,54,174,6964,23219,31995,23219,34835,43736,75117,31795,88063,33,5,112,68641,87,74,4518,49250,14240,40689,80558,40685,40606,68869,73374,45472,101483,19926,42714,11755,46801,62695,40712,44,9338,26957,56276,56276,21)")
	#--May-----
	elif monthIndex == 4:
		layer.SetAttributeFilter("VoyageId not in (3501,5,19779,7598,27371,3471,176,3494,6557,124,48310,9902,30968,88860,13144,63312,19765,74582,56817,73541,84404,68096,64737,38900,65093,36983,53,149,38234,16532,48303,52545,13312,22123,43,149,16522,121637,95833,91889,30989,28594,44665,9877,34633,52,32694,30,30592,50503,6524,16566,21389,52,42162,50349,46635,15809,6530,22,13289,27343,75710,52515,3526,56814,28221,48113,63365,109313,23350,40733,42543,38904,25488,100800,78654,51379,19755,24,33,29220,27357,27350,41364,19763,80106,70933,92767,9879,20865,67,40,39,39)")
	#--June---
	elif monthIndex == 5:
		layer.SetAttributeFilter("VoyageId not in (183,920,156)")
	##----July----
	elif monthIndex == 6:
		layer.SetAttributeFilter("VoyageId not in (89,13622,14,151,2184,80,19184,33640,12520,12518,202,71344,12819,4089,23339,21342,5734,98,274,32924,24492,72871,84281,21593,7701,5025,9770,29812,8791,4077,145,8514,317,21171,11717,18441,21645,67561,47072,37429,7472,143,79893,36,34282,2189,27,66590,60853,181,55297,16736,12708,231,9804,5108,19443,4105,74602,63145,120,129,19958,11854,258,65084,23178,251,67182,15050,62979,1463,60,30654,80171,19436,22994,2179,25370,21271,52363,23803,64324,75014,13129,2163,208,13189,11094,11708,27170,13634,58715,163,62425,27233,48731,7628,80209,82608,74950,15735,11499,2603,76724,36245,1320,10753,4032,5272,7720,4896,127,78,1403,11728,93,80584,70264,11722,13682,51291,16978,110,45189,27208,38352,5730,179,194,3593,39342,61819)")
	##--August
	elif monthIndex == 7:
		layer.SetAttributeFilter("VoyageId not in (88466,13832,61821,95629,32876,18478,5,18473,47323,12660,6081,116980,102909,27686,12169,14,36812,6734,57,38015,982,41726,82538,68,326,100,12984,12878,57625,94498,7101,113105,345,1910,61712,32320,41524,8,42225,98815,335,203,39357,97689,17599,18818,92,6828,61561,10588,13646,105259,12429,12012,4915,27727,78520,107466,33585,83082,2844,120,206,4742,5964,55462,71010,95861,83238,5772,2012,244,29665,22,5312,57083,13850,47914,34578,9035,1996,44567,4578,56610,1921,42899,61715,53,76,9,62916,73490,62916,48818,52906,63,9949,72,168,53652,3777,37732,73979,83921,93173,5597,38080,6086,71992,5339,27818,26193,39364,32399,5322,18471,3744,81377,81888,21790,102837,39799,11643,98,242,29779,27523,105,29816,54,1929,34806,18573,106512,36)")

	##---September---
	elif monthIndex == 8:
		layer.SetAttributeFilter("VoyageId not in (8674,40935,25774,13004,125,78,12408,7778,102448,97,2408,4610,193,55885,34820,121,126,72054,250,16567,314,28197,190,67353,27766,31991,109815,55898,186,90861,67122,335,36120,174,3942,25141,71,195,308,2992,72280,73688,68216,52644,75548,78201,122444,68219,52626,62740,67632,102,120731,44,2183,48583,22207,89097,12412,73211,34415,71238,14376,97194,131113,50260,34424,207,91492,55697,77954,123625,12979,115800,42,43011,110618,76638,8699,52629,8267,90991,102438,37974,39291,12999,179,8713,54715,100200,17928,83238,119785,71192,120428,27898,88,84843,211,28040,281,327,57074,24267,33653,201,112691,20914,8702,34822,37715,24508,215,315,39085,28587,38,17943,26,60,323,39262,291,16493,126300,28320,25812,42751,45736,45736,115655,113912,88206,44355)")
	##---Octomber---
	elif monthIndex == 9:
		layer.SetAttributeFilter("VoyageId not in (7040,4983,27195,116017,27664,14455,1202,108774,119,7631,108941,3626,77,9360,4968,82509,7086,6028,96584,143,24440,1316,76913,2975,13889,108720,6566,9596,101,78667,55883,3600,3558,116020,4967,43485,53,2209,44987,29250,62351,85469,1269,123009,9647,53126,41701,40236,43101,16,37433,37433,50,46)")
	#--November--
	elif monthIndex == 10:
		layer.SetAttributeFilter("VoyageId not in (43085,75,63202,26104,6,123470,16882,14984,37,74579,49909,218,52373,34,122424,11973,7745,30592,16886,70735,78472,7532,40504,16914,64768,66919,3413,39899,49046,154,78653,86948,56429,59758,74578,74601,2,48355)")
	##-December---
	elif monthIndex == 11:
		layer.SetAttributeFilter("VoyageId not in (29753,45838,50941,5038,58404,62,33,14557,37296,29696,77,62816,4078,39840,52880,20168,21429,21438,45492,24316,38473,42900,57062,62859,8236,42918,20861,144,36139,5022,68882,24303,25322,86091,24299,34833,58062,32436,61726,37919,51260,40497,41525,14551,199,86793,66024,18203,48439,34615,56525,27287,54248,46646,51058,24319,83440,5000,32445,74315,18191,21103,68,14573,81119,31190,62738,76862,86836,86858,86857,90951,54,56871,79876,101,81112,75081,27497,26428,17,17)")

	broadcastDict = dict()
	cnt = 0
	c = 0
	for feature in layer:
		geom = feature.GetGeometryRef()
		mmsi = feature['MMSI']
		vId = months[monthIndex] + '_' + str(feature['VoyageId'])
		if vId in voyageDict:
			if mmsi not in broadcastDict:
				broadcastDict[mmsi] = dict()
				broadcastDict[mmsi][vId] = {'Geometry' : [[geom.GetX(), geom.GetY()]], 'DateTime' : [feature['BaseDateTime']], 'MMSI' : mmsi}
			else:
				if vId not in broadcastDict[mmsi]:
					broadcastDict[mmsi][vId] = {'Geometry' : [[geom.GetX(), geom.GetY()]], 'DateTime' : [feature['BaseDateTime']], 'MMSI' : mmsi}
				else:
					broadcastDict[mmsi][vId]['Geometry'].append([geom.GetX(), geom.GetY()])
					broadcastDict[mmsi][vId]['DateTime'].append(feature['BaseDateTime'])
			cnt = cnt + 1

	for mmsi in broadcastDict:
		for vId in broadcastDict[mmsi]:
			dest[voyageDict[vId]['Destination']] = voyageDict[vId]['Destination']


	geojson = []
	menuJson = []
	chk_len = 0
	for mmsi in broadcastDict:
	
		voyages = []
		for vId in broadcastDict[mmsi]:
			voyages.append(vId)
			
			geojson.append({"type": "Feature", "geometry": {"type": "LineString","coordinates": broadcastDict[mmsi][vId]['Geometry']},"properties": {"voyage": vId,'MMSI' : mmsi,'Name' : vesselDict[mmsi]['Name'],'Type' : vesselDict[mmsi]['VesselType'],'Destination' : voyageDict[vId]['Destination'],'Cargo' : voyageDict[vId]['Cargo'],'IMO' : vesselDict[mmsi]['IMO'], 'Region' : str(mmsi)[:1]}})
		
		menuJson.append({'MMSI' : mmsi,"Voyages" : voyages})
		#allMenuJson.append({'MMSI' : mmsi,"Voyages" : voyages, 'Continuous' : continuousVoyage[mmsi]})

		if mmsi not in globalBroadcast:
			globalBroadcast[mmsi] = broadcastDict[mmsi]
		else:
			for vId in broadcastDict[mmsi]:
				globalBroadcast[mmsi][vId] = broadcastDict[mmsi][vId]

	with open('/Users/nilesh/Project/menu/'+months[monthIndex]+'_menu.json', 'w') as outfile:
		json.dump(menuJson, outfile)

	with open('/Users/nilesh/Project/GeoJson/'+monthsLower[monthIndex]+'_voyages.geojson', 'w') as outfile:
		json.dump({ "type": "FeatureCollection", "features": geojson}, outfile)

	monthIndex = monthIndex + 1

#End for loop

fmt = '%Y/%m/%d %H:%M:%S'
continuousVoyage = dict()

for mmsi in globalBroadcast:
		voy = []
		for vId in globalBroadcast[mmsi]:
			voy.append(vId)
		cont = []
		for i in range(0,len(voy)):
			l1 = len(globalBroadcast[mmsi][voy[i]]['DateTime'])
			d1 = datetime.strptime(globalBroadcast[mmsi][voy[i]]['DateTime'][l1-1], fmt)
			temp = [voy[i]]
			existFlag = -1
			
			for t in cont:
				if voy[i] in t:
					temp = t
					existFlag = 1
			
			for j in range(i+1,len(voy)):
				d2 = datetime.strptime(globalBroadcast[mmsi][voy[j]]['DateTime'][0], fmt)
				if d1.month - d2.month == 1:
					if ((d1-d2).days * 24 * 60) <= 5:
						temp.append(voy[j])
						break

			if existFlag == -1:
				cont.append(temp)

		continuousVoyage[mmsi] = cont

		allMenuJson.append({'MMSI' : mmsi,"Voyages" : continuousVoyage[mmsi]})

sortedDestination = collections.OrderedDict(sorted(dest.items()))

destArray = []
for key, value in sortedDestination.iteritems() :
    destArray.append(key)

with open('/Users/nilesh/Project/destination/destination.json', 'w') as outfile:
	json.dump(destArray, outfile)

with open('/Users/nilesh/Project/menu/all_menu.json', 'w') as outfile:
	json.dump(allMenuJson, outfile)