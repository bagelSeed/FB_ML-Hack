from math import sqrt
# ref = set((long, lat, val))
parsed_data = {}

def fn(lat, lon, ref):
	ret = [0.0, 0.0]
	d_tot = 0.0
	for data in ref:
		d_lat, d_lon, _, _ = data
		d_tot += 1.0/getDist(lon, lat, d_lon, d_lat)

	for data in ref:
		d_lat, d_lon, air, ground = data
		dist = getDist(lon, lat, d_lon, d_lat)
		ret[0] += (1.0/dist)/d_tot * air
		ret[1] += (1.0/dist)/d_tot * ground

	return ret


def getDist(h_lon, h_lat, t_lon, t_lat):

	h_lon = float(h_lon)
	h_lat = float(h_lat)
	dx = abs(h_lon - t_lon)
	dy = abs(h_lat - t_lat)
	return sqrt(dx*dx + dy*dy)

def parseLoc():
	with open('./Road_Weather_Clean2 (1).csv', 'r') as f:
		for line in f:
			name, lat, lon, date, air, ground = line.strip().split(',')
			if date not in parsed_data:
				parsed_data[date] = []

			parsed_data[date].append((float(lat), float(lon), float(air), float(ground)))


def parseFire():
	g = open("./output.csv", "w")
	g.write("@relation fire\n@attribute lat numeric\n@attribute lon numeric\n@attribute airtemp numeric\n@attribute groundtemp numeric\n@attribute seconds numeric\n@attribute fire {Y, N}\n@data\n")
	with open('./Seattle_Real_Time_Fire_911_Calls.csv', 'r') as f:
		for line in f:
			parts = line.strip().split(",")
			if len(parts) != 8:
				continue
			_, _, date, lat, lon, _, _, _ = parts
			if len(date.split(" ")) != 4 or not lat or not lon:
				continue
			day, time, pm, _ = date.split(" ")
			hr, _, _ = time.split(':')
			hr = int(hr)
			if (hr == 12 and pm == 'AM'):
				hr = 0
			elif (hr != 12 and pm == 'PM'):
				hr += 12
			date = day + " %.2d" % hr

			if date in parsed_data:
				air, ground = fn(lat, lon, parsed_data[date])
				g.write((lat + ',' + lon + ',%.2f,%.2f,%d,Y\n') % (air, ground, hr))

	g.close()

parseLoc()
parseFire()


