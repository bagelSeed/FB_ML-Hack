from geopy.geocoders import Nominatim
import csv
geolocator = Nominatim()
with open('Traffic_Flow_Counts.csv', 'rb') as csvinput:
	reader = csv.reader(csvinput)
	with open('traffic_with_coordinate_estimates.csv', 'wb') as output:
		writer = csv.writer(output, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		for row in reader:
			street = row[1]
			if street == "STNAME":
				writer.writerow(["STNAME", "LATITUDE", "LONGITUDE"])
				continue

			address = street + " Seattle"
			try:
				location = geolocator.geocode(address)
				if location == None:
					print "No location for " + address
					continue
				output_row = [street, location.latitude, location.longitude]
				writer.writerow(output_row)
			except:
				print "Timed out for " + address
				continue

			

